import os
import base64
from email.mime.text import MIMEText
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from dotenv import load_dotenv

load_dotenv("../.env")

# Assumes you have already completed OAuth2 flow and have a token.json file with user credentials
# For production, implement a full OAuth2 flow with refresh token handling

def get_gmail_service():
    creds = None
    SCOPES = [
        "https://www.googleapis.com/auth/gmail.readonly",
        "https://www.googleapis.com/auth/gmail.send"
    ]
    if os.path.exists("token.json"):
        creds = Credentials.from_authorized_user_file("token.json", SCOPES)
        # Check if the credentials have the required scopes
        if not creds or not creds.has_scopes(SCOPES):
            raise Exception(
                "Your token.json does not have the required Gmail API scopes. "
                "Please delete token.json and re-run the authentication flow to grant both read and send permissions."
            )
    else:
        raise Exception(
            "token.json not found. Please complete the OAuth2 flow for Gmail API. "
            "You must grant both read and send permissions."
        )
    service = build("gmail", "v1", credentials=creds)
    return service

def send_gmail(recipient: str, subject: str, body: str) -> dict:
    """Send an email via Gmail using the Gmail API."""
    try:
        service = get_gmail_service()
        message = MIMEText(body)
        message["to"] = recipient
        message["subject"] = subject
        raw = base64.urlsafe_b64encode(message.as_bytes()).decode()
        message_body = {"raw": raw}
        sent_message = (
            service.users().messages().send(userId="me", body=message_body).execute()
        )
        return {"status": "success", "id": sent_message["id"]}
    except Exception as e:
        return {"status": "error", "message": str(e)}

def get_recent_emails(max_results: int = 5) -> dict:
    """Retrieve the most recent emails from the user's Gmail inbox."""
    try:
        service = get_gmail_service()
        results = service.users().messages().list(userId="me", maxResults=max_results, labelIds=["INBOX"]).execute()
        messages = results.get("messages", [])
        emails = []
        for msg in messages:
            msg_detail = service.users().messages().get(userId="me", id=msg["id"]).execute()
            headers = msg_detail.get("payload", {}).get("headers", [])
            subject = next((h["value"] for h in headers if h["name"] == "Subject"), "(No Subject)")
            sender = next((h["value"] for h in headers if h["name"] == "From"), "(Unknown Sender)")
            snippet = msg_detail.get("snippet", "")
            emails.append({
                "id": msg["id"],
                "subject": subject,
                "from": sender,
                "snippet": snippet
            })
        return {"status": "success", "emails": emails}
    except Exception as e:
        return {"status": "error", "message": str(e)}


def get_many_emails(query: str = '', max_results: int = 20) -> dict:
    """
    Retrieve emails matching a Gmail search query (e.g., subject or keyword).
    - query: Gmail search string (e.g., 'subject:"DRC Order Receipt"')
    - max_results: maximum number of emails to return
    """
    try:
        service = get_gmail_service()
        results = service.users().messages().list(userId="me", maxResults=max_results, q=query).execute()
        messages = results.get("messages", [])
        emails = []
        for msg in messages:
            msg_detail = service.users().messages().get(userId="me", id=msg["id"]).execute()
            headers = msg_detail.get("payload", {}).get("headers", [])
            subject = next((h["value"] for h in headers if h["name"] == "Subject"), "(No Subject)")
            sender = next((h["value"] for h in headers if h["name"] == "From"), "(Unknown Sender)")
            snippet = msg_detail.get("snippet", "")
            emails.append({
                "id": msg["id"],
                "subject": subject,
                "from": sender,
                "snippet": snippet
            })
        return {"status": "success", "emails": emails}
    except Exception as e:
        return {"status": "error", "message": str(e)}

def reply_to_email(message_id: str, body: str, subject: str = "") -> dict:
    """Reply to an email by message ID. Optionally override the subject."""
    try:
        service = get_gmail_service()
        # Fetch the original message to get threadId and headers
        original = service.users().messages().get(userId="me", id=message_id, format="metadata", metadataHeaders=["Subject", "From", "To", "Message-ID"]).execute()
        thread_id = original.get("threadId")
        headers = original.get("payload", {}).get("headers", [])
        orig_subject = next((h["value"] for h in headers if h["name"] == "Subject"), "")
        orig_from = next((h["value"] for h in headers if h["name"] == "From"), "")
        orig_to = next((h["value"] for h in headers if h["name"] == "To"), "")
        orig_msg_id = next((h["value"] for h in headers if h["name"] == "Message-ID"), None)
        reply_subject = subject if subject else ("Re: " + orig_subject if not orig_subject.lower().startswith("re:") else orig_subject)

        # Compose reply headers
        reply_headers = []
        if orig_msg_id:
            reply_headers.append(("In-Reply-To", orig_msg_id))
            reply_headers.append(("References", orig_msg_id))

        # Construct the reply message
        from email.mime.text import MIMEText
        import base64
        msg = MIMEText(body)
        msg["to"] = orig_from
        msg["subject"] = reply_subject
        for k, v in reply_headers:
            msg[k] = v
        raw = base64.urlsafe_b64encode(msg.as_bytes()).decode()
        message_body = {"raw": raw, "threadId": thread_id}
        sent_message = service.users().messages().send(userId="me", body=message_body).execute()
        return {"status": "success", "id": sent_message["id"]}
    except Exception as e:
        return {"status": "error", "message": str(e)}

def get_unread_emails(max_results: int = 5) -> dict:
    """Retrieve the most recent unread emails from the user's Gmail inbox."""
    try:
        service = get_gmail_service()
        results = service.users().messages().list(userId="me", maxResults=max_results, labelIds=["INBOX", "UNREAD"]).execute()
        messages = results.get("messages", [])
        emails = []
        for msg in messages:
            msg_detail = service.users().messages().get(userId="me", id=msg["id"]).execute()
            headers = msg_detail.get("payload", {}).get("headers", [])
            subject = next((h["value"] for h in headers if h["name"] == "Subject"), "(No Subject)")
            sender = next((h["value"] for h in headers if h["name"] == "From"), "(Unknown Sender)")
            snippet = msg_detail.get("snippet", "")
            emails.append({
                "id": msg["id"],
                "subject": subject,
                "from": sender,
                "snippet": snippet
            })
        return {"status": "success", "emails": emails}
    except Exception as e:
        return {"status": "error", "message": str(e)}

def delete_email(message_id: str) -> dict:
    """Delete an email from the user's Gmail account by message ID."""
    try:
        service = get_gmail_service()
        service.users().messages().delete(userId="me", id=message_id).execute()
        return {"status": "success", "message": f"Email with ID {message_id} deleted."}
    except Exception as e:
        return {"status": "error", "message": str(e)}
