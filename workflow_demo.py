# workflow_demo.py

from google.adk.sessions import InMemorySessionService

# --- External API Integrations ---
# Ensure you have set up your .env with GITHUB_TOKEN, GITHUB_USERNAME, and that Google API token.json is present.
# For Google Sheets, fill in your actual spreadsheet ID and range below.

from manager.sub_agents.coding_agent.tools.github_tool import create_github_repo
from manager.sub_agents.scraper_agent.scraper_tool import selenium_scrape_headlines
from manager.sub_agents.google_agent.sheets_tools import append_sheet, list_sheets
from googleapiclient.discovery import build
from google.oauth2.credentials import Credentials
from dotenv import load_dotenv

load_dotenv(".env")

import os
print("GITHUB_TOKEN:", os.getenv("GITHUB_TOKEN"))
print("GITHUB_USERNAME:", os.getenv("GITHUB_USERNAME"))

import sys
print("sys.path:", sys.path)

def create_sheet(sheet_name: str) -> dict:
    """Create a new Google Sheet with the given name and return its ID."""
    creds = None
    if os.path.exists("token.json"):
        creds = Credentials.from_authorized_user_file("token.json", ["https://www.googleapis.com/auth/spreadsheets"])
    else:
        return {"status": "error", "message": "token.json not found. Please complete OAuth2 flow for Google Sheets API."}
    try:
        service = build("sheets", "v4", credentials=creds)
        spreadsheet = {
            'properties': {
                'title': sheet_name
            }
        }
        sheet = service.spreadsheets().create(body=spreadsheet, fields='spreadsheetId').execute()
        return {"status": "success", "spreadsheetId": sheet.get('spreadsheetId')}
    except Exception as e:
        return {"status": "error", "message": str(e)}

# 1. Create a session service and a new session
session_service = InMemorySessionService()
session = session_service.create_session(
    app_name="agent4_app",
    user_id="user_demo",
    session_id="session_demo"
)

# 2. Store a user request in shared memory
session.state['last_user_request'] = "Please scrape a website, log results to Google Sheets, and create a repo for the code."

# 3. Coding agent creates a GitHub repo using the real API
import datetime

repo_name = f"my-demo-repo-{datetime.datetime.now().strftime('%Y%m%d%H%M%S%f')}"
github_result = create_github_repo(repo_name, private=True, description="Demo repo created by agent workflow.")
session.state['github_result'] = github_result
print("GitHub Repo Creation Result:")
print(github_result)
print("-" * 40)

# 4. Scraper agent scrapes real data from a website
url = "https://example.com"
scrape_result = selenium_scrape_headlines(url)
session.state['scrape_result'] = scrape_result
print("Web Scraping Result:")
print(scrape_result)
print("-" * 40)

# 5. Google Sheets: append scraped headlines
SHEET_IDENTIFIER = "Demo Results"  # or your sheet ID
sheet_range = "Sheet1!A1"

# List all available Google Sheets for debugging and selection
sheets_listing = list_sheets()
if sheets_listing.get('status') == 'success':
    print("Available Google Sheets:")
    for s in sheets_listing['sheets']:
        print(f"  - {s['name']} (ID: {s['id']})")
else:
    print(f"ERROR: Could not list Google Sheets: {sheets_listing.get('message')}")

spreadsheet_id = SHEET_IDENTIFIER
sheet_found = False
if not (len(SHEET_IDENTIFIER) == 44 and '-' in SHEET_IDENTIFIER):  # crude check for ID
    if sheets_listing.get('status') == 'success':
        matches = [s for s in sheets_listing['sheets'] if s['name'].lower() == SHEET_IDENTIFIER.lower()]
        if matches:
            spreadsheet_id = matches[0]['id']
            sheet_found = True
            print(f"Found Google Sheet ID for '{SHEET_IDENTIFIER}': {spreadsheet_id}")
        else:
            print(f"No Google Sheet found with name '{SHEET_IDENTIFIER}'. Creating new sheet...")
            create_result = create_sheet(SHEET_IDENTIFIER)
            print("Sheet creation result:", create_result)
            if create_result.get('status') == 'success':
                spreadsheet_id = create_result['spreadsheetId']
                sheet_found = True
                print(f"Created and using new Google Sheet with ID: {spreadsheet_id}")
            else:
                spreadsheet_id = None
                print("ERROR: Failed to create new Google Sheet.")
    else:
        print(f"ERROR: Could not list Google Sheets: {sheets_listing.get('message')}")
        spreadsheet_id = None
else:
    sheet_found = True

headlines = scrape_result['headlines'] if scrape_result.get('status') == 'success' else []
values = [[h] for h in headlines]
gsheets_result = None
if spreadsheet_id and sheet_found:
    gsheets_result = append_sheet(spreadsheet_id, sheet_range, values)
    session.state['google_sheets_result'] = gsheets_result
    print("Google Sheets Logging Result:")
    print(gsheets_result)
    print("-" * 40)
else:
    print("Skipping Google Sheets append due to missing or invalid spreadsheet ID.")

# --- Logging and Memory Updates ---
session.state.setdefault('actions', []).append({
    "agent": "coding_agent",
    "action": "create_github_repo",
    "result": github_result
})
session.state.setdefault('actions', []).append({
    "agent": "scraper_agent",
    "action": "selenium_scrape_headlines",
    "result": scrape_result
})
if gsheets_result:
    session.state.setdefault('actions', []).append({
        "agent": "google_agent",
        "action": "append_sheet",
        "result": gsheets_result
    })

session.state['coding_agent_last_task'] = github_result
session.state['scraper_agent_last_task'] = scrape_result
session.state['google_agent_last_task'] = gsheets_result

# Print logs
print("Full Shared Action Log:")
for action in session.state.get('actions', []):
    print(action)

print("\nAgent-Specific Last Task Memory:")
print("Last coding agent task:", session.state.get('coding_agent_last_task'))
print("Last scraper agent task:", session.state.get('scraper_agent_last_task'))
print("Last google agent task:", session.state.get('google_agent_last_task'))

# 5. Google agent handles a task
# (Google Sheets logging is now handled via append_sheet; no need to call handle_google_task)

# 6. Retrieve and print the full shared action log
print("Full Shared Action Log:")
for action in session.state.get('actions', []):
    print(action)

# 7. Show agent-specific last task memory
print("\nAgent-Specific Last Task Memory:")
print("Last coding agent task:", session.state.get('coding_agent_last_task'))
print("Last scraper agent task:", session.state.get('scraper_agent_last_task'))
print("Last google agent task:", session.state.get('google_agent_last_task'))