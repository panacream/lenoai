import os
from typing import List, Dict
from googleapiclient.discovery import build
from google.oauth2.credentials import Credentials


def get_drive_service():
    """Get the Google Drive API service using stored credentials."""
    creds = None
    if os.path.exists("token.json"):
        creds = Credentials.from_authorized_user_file("token.json", [
            "https://www.googleapis.com/auth/drive.metadata.readonly"
        ])
    else:
        raise Exception("token.json not found. Please complete OAuth2 flow for Google Drive API.")
    service = build("drive", "v3", credentials=creds)
    return service


def list_sheets() -> dict:
    """List all Google Sheets files accessible to the user (name and ID)."""
    try:
        service = get_drive_service()
        results = service.files().list(
            q="mimeType='application/vnd.google-apps.spreadsheet' and trashed=false",
            fields="files(id, name)",
            pageSize=1000
        ).execute()
        files = results.get('files', [])
        sheets = [{"id": f["id"], "name": f["name"]} for f in files]
        return {"status": "success", "sheets": sheets}
    except Exception as e:
        return {"status": "error", "message": str(e)}

def get_sheets_service():
    """Get the Google Sheets API service using stored credentials."""
    creds = None
    if os.path.exists("token.json"):
        creds = Credentials.from_authorized_user_file("token.json", [
            "https://www.googleapis.com/auth/spreadsheets"
        ])
    else:
        raise Exception("token.json not found. Please complete OAuth2 flow for Google Sheets API.")
    service = build("sheets", "v4", credentials=creds)
    return service


def read_sheet(spreadsheet_id: str, range_: str) -> Dict[str, any]:
    """Read values from a Google Sheet given spreadsheet ID and range (e.g. 'Sheet1!A1:C10')."""
    try:
        service = get_sheets_service()
        sheet = service.spreadsheets()
        result = sheet.values().get(spreadsheetId=spreadsheet_id, range=range_).execute()
        values = result.get('values', [])
        return {"status": "success", "values": values}
    except Exception as e:
        return {"status": "error", "message": str(e)}


def write_sheet(spreadsheet_id: str, range_: str, values: List[List[str]]) -> Dict[str, any]:
    """Write values to a Google Sheet given spreadsheet ID, range, and values (2D list of strings)."""
    try:
        service = get_sheets_service()
        body = {'values': values}
        sheet = service.spreadsheets()
        result = sheet.values().update(
            spreadsheetId=spreadsheet_id,
            range=range_,
            valueInputOption="RAW",
            body=body
        ).execute()
        return {"status": "success", "updatedCells": result.get('updatedCells', 0)}
    except Exception as e:
        return {"status": "error", "message": str(e)}


def append_sheet(spreadsheet_id: str, range_: str, values: List[List[str]]) -> Dict[str, any]:
    """Append values to a Google Sheet given spreadsheet ID, range, and values (2D list of strings)."""
    try:
        service = get_sheets_service()
        body = {'values': values}
        sheet = service.spreadsheets()
        result = sheet.values().append(
            spreadsheetId=spreadsheet_id,
            range=range_,
            valueInputOption="RAW",
            insertDataOption="INSERT_ROWS",
            body=body
        ).execute()
        return {"status": "success", "updates": result.get('updates', {})}
    except Exception as e:
        return {"status": "error", "message": str(e)}


def describe_sheet(spreadsheet_id: str) -> dict:
    """Describe the structure of a Google Sheet: sheet names, columns (headers), and all populated rows for each sheet/tab."""
    try:
        service = get_sheets_service()
        # Get sheet metadata (to list all sheets/tabs)
        meta = service.spreadsheets().get(spreadsheetId=spreadsheet_id).execute()
        sheets_data = []
        for sheet_info in meta.get("sheets", []):
            title = sheet_info["properties"]["title"]
            # Get all values for this sheet
            result = service.spreadsheets().values().get(
                spreadsheetId=spreadsheet_id,
                range=title
            ).execute()
            values = result.get("values", [])
            headers = values[0] if values else []
            rows = values[1:] if len(values) > 1 else []
            sheets_data.append({
                "sheet_name": title,
                "columns": headers,
                "rows": rows
            })
        return {"status": "success", "sheets": sheets_data}
    except Exception as e:
        return {"status": "error", "message": str(e)}


def extract_and_log_order_receipts(sheet_name: str, sheet_tab: str = "Sheet1", email_query: str = "order receipt", max_emails: int = 10) -> dict:
    """
    Extract order receipts from Gmail and append them to the specified Google Sheet.
    - sheet_name: Name of the Google Sheet (not ID)
    - sheet_tab: Name of the tab within the sheet
    - email_query: Gmail search query (e.g., subject or label)
    - max_emails: Max emails to process
    """
    try:
        # 1. Find the sheet ID
        from .gmail_tools import get_unread_emails
        sheets_result = list_sheets()
        if sheets_result["status"] != "success":
            return {"status": "error", "message": "Could not list sheets."}
        sheet_id = next((s["id"] for s in sheets_result["sheets"] if s["name"] == sheet_name), None)
        if not sheet_id:
            return {"status": "error", "message": f"Sheet '{sheet_name}' not found."}

        # 2. Get columns
        desc = describe_sheet(sheet_id)
        if desc["status"] != "success":
            return {"status": "error", "message": "Could not describe sheet."}
        columns = next((s["columns"] for s in desc["sheets"] if s["sheet_name"] == sheet_tab), None)
        if not columns:
            # Try to auto-create the tab with default headers if not found
            available_tabs = [s["sheet_name"] for s in desc["sheets"]]
            # Default headers for order receipts
            default_headers = ["Order Number", "Order Date", "Order Total"]
            try:
                service = get_sheets_service()
                # Add new sheet/tab
                add_sheet_request = {
                    "requests": [{
                        "addSheet": {
                            "properties": {"title": sheet_tab}
                        }
                    }]
                }
                service.spreadsheets().batchUpdate(
                    spreadsheetId=sheet_id,
                    body=add_sheet_request
                ).execute()
                # Write headers to new tab
                write_sheet(sheet_id, f"{sheet_tab}!A1", [default_headers])
                columns = default_headers
            except Exception as e:
                return {"status": "error", "message": f"Tab '{sheet_tab}' not found. Available tabs: {available_tabs}. Tried to auto-create but failed: {e}"}
        if not columns:
            return {"status": "error", "message": f"Could not determine columns for tab '{sheet_tab}'. Available tabs: {available_tabs}"}

        # 3. Get relevant emails (here: get unread emails, could be replaced with a specific query)
        emails_result = get_unread_emails(max_results=max_emails)
        if emails_result["status"] != "success":
            return {"status": "error", "message": "Could not retrieve emails."}
        emails = emails_result["emails"]

        # 4. Parse order details and prepare rows
        def parse_order_email(snippet: str) -> dict:
            # Example regex for Amazon-like order: "Order #123-4567890-1234567 on May 1, 2025 Total $12.34"
            import re
            order = {}
            order_number = re.search(r"Order[\s#:]*([\w-]+)", snippet)
            date = re.search(r"on ([A-Za-z]+ \d{1,2}, \d{4})", snippet)
            total = re.search(r"Total \$([\d,.]+)", snippet)
            if order_number:
                order["Order Number"] = order_number.group(1)
            if date:
                order["Order Date"] = date.group(1)
            if total:
                order["Order Total"] = total.group(1)
            # Add more parsing as needed
            return order

        rows_to_append = []
        for email in emails:
            order_data = parse_order_email(email.get("snippet", ""))
            row = [order_data.get(col, "") for col in columns]
            rows_to_append.append(row)

        # 5. Append to sheet
        res = append_sheet(sheet_id, f"{sheet_tab}!A1", rows_to_append)
        return {"status": "success", "appended_rows": len(rows_to_append), "details": res}
    except Exception as e:
        return {"status": "error", "message": str(e)}
