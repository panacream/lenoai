import os
from typing import List, Dict, Any, Optional
from datetime import datetime
from googleapiclient.discovery import build
from google.oauth2.credentials import Credentials

CALENDAR_SCOPES = ["https://www.googleapis.com/auth/calendar"]

def get_calendar_service():
    """Get the Google Calendar API service using stored credentials."""
    import os
    creds = None
    # Always look for token.json in the google_agent directory
    token_path = os.path.join(os.path.dirname(__file__), "../token.json")
    token_path = os.path.abspath(token_path)
    if os.path.exists(token_path):
        creds = Credentials.from_authorized_user_file(token_path, CALENDAR_SCOPES)
    else:
        raise Exception(f"token.json not found at {token_path}. Please complete OAuth2 flow for Google Calendar API.")
    service = build("calendar", "v3", credentials=creds)
    return service

def list_upcoming_events(calendar_id: str = 'primary', max_results: int = 10) -> List[Dict[str, Any]]:
    """
    List upcoming events from a Google Calendar.
    Args:
        calendar_id (str): Calendar ID to fetch events from (default: 'primary').
        max_results (int): Maximum number of events to return (default: 10).
    Returns:
        List of event dicts with summary, start, end, and eventId.
    """
    service = get_calendar_service()
    now = datetime.utcnow().isoformat() + 'Z'
    events_result = service.events().list(
        calendarId=calendar_id,
        timeMin=now,
        maxResults=max_results,
        singleEvents=True,
        orderBy='startTime'
    ).execute()
    events = events_result.get('items', [])
    return [
        {
            'summary': e.get('summary'),
            'start': e['start'].get('dateTime', e['start'].get('date')),
            'end': e['end'].get('dateTime', e['end'].get('date')),
            'eventId': e.get('id')
        } for e in events
    ]

def create_event(calendar_id: str = 'primary', summary: str = '', start_time: str = '', end_time: str = '', description: Optional[str] = None, attendees: Optional[List[str]] = None) -> Dict[str, Any]:
    """
    Create a new event in Google Calendar.
    Args:
        calendar_id (str): Calendar ID (default: 'primary').
        summary (str): Event title.
        start_time (str): ISO 8601 start datetime (e.g., '2025-05-30T17:00:00Z').
        end_time (str): ISO 8601 end datetime.
        description (str, optional): Event description.
        attendees (list of str, optional): List of attendee emails.
    Returns:
        The created event object.
    """
    service = get_calendar_service()
    event = {
        'summary': summary,
        'start': {'dateTime': start_time},
        'end': {'dateTime': end_time},
    }
    if description:
        event['description'] = description
    if attendees:
        event['attendees'] = [{'email': email} for email in attendees]
    created_event = service.events().insert(calendarId=calendar_id, body=event).execute()
    return created_event

def update_event(calendar_id: str, event_id: str, summary: Optional[str] = None, start_time: Optional[str] = None, end_time: Optional[str] = None, description: Optional[str] = None, attendees: Optional[List[str]] = None) -> Dict[str, Any]:
    """
    Update an existing event in Google Calendar.
    Args:
        calendar_id (str): Calendar ID.
        event_id (str): ID of the event to update.
        summary (str, optional): New event title.
        start_time (str, optional): New ISO 8601 start datetime.
        end_time (str, optional): New ISO 8601 end datetime.
        description (str, optional): New description.
        attendees (list of str, optional): New list of attendee emails.
    Returns:
        The updated event object.
    """
    service = get_calendar_service()
    event = service.events().get(calendarId=calendar_id, eventId=event_id).execute()
    if summary:
        event['summary'] = summary
    if start_time:
        event['start']['dateTime'] = start_time
    if end_time:
        event['end']['dateTime'] = end_time
    if description:
        event['description'] = description
    if attendees is not None:
        event['attendees'] = [{'email': email} for email in attendees]
    updated_event = service.events().update(calendarId=calendar_id, eventId=event_id, body=event).execute()
    return updated_event


def delete_event(calendar_id: str, event_id: str) -> Dict[str, Any]:
    """
    Delete an event from Google Calendar.
    Args:
        calendar_id (str): Calendar ID.
        event_id (str): Event ID to delete.
    Returns:
        Dict with 'success': True if deleted, or error message.
    """
    service = get_calendar_service()
    try:
        service.events().delete(calendarId=calendar_id, eventId=event_id).execute()
        return {'success': True}
    except Exception as e:
        return {'success': False, 'error': str(e)}

def get_event_details(calendar_id: str, event_id: str) -> Dict[str, Any]:
    """
    Get details of a specific event from Google Calendar.
    Args:
        calendar_id (str): Calendar ID.
        event_id (str): Event ID.
    Returns:
        Event object dict or error.
    """
    service = get_calendar_service()
    try:
        event = service.events().get(calendarId=calendar_id, eventId=event_id).execute()
        return event
    except Exception as e:
        return {'error': str(e)}
