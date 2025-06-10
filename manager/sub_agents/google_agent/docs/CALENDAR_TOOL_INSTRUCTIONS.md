# Google Calendar Tool Instructions

This document describes the available Google Calendar tools for the Google agent. Each tool is registered and can be called by the agent to interact with the Google Calendar API for a variety of scheduling and event management tasks.

---

## list_upcoming_events
**Purpose:** List upcoming events from a Google Calendar.

**Arguments:**
- `calendar_id` (str, optional): Calendar ID to fetch events from (default: 'primary').
- `max_results` (int, optional): Maximum number of events to return (default: 10).

**Returns:**
- List of event dicts with `summary`, `start`, `end`, and `eventId`.

**Example:**
```python
list_upcoming_events(calendar_id='primary', max_results=5)
```

---

## create_event
**Purpose:** Create a new event in Google Calendar.

**Arguments:**
- `calendar_id` (str, optional): Calendar ID (default: 'primary').
- `summary` (str): Event title.
- `start_time` (str): ISO 8601 start datetime (e.g., '2025-05-30T17:00:00Z').
- `end_time` (str): ISO 8601 end datetime.
- `description` (str, optional): Event description.
- `attendees` (list of str, optional): List of attendee emails.

**Returns:**
- The created event object.

**Example:**
```python
create_event(summary="Meeting", start_time="2025-05-30T17:00:00Z", end_time="2025-05-30T18:00:00Z", description="Discuss roadmap", attendees=["user@example.com"])
```

---

## update_event
**Purpose:** Update an existing event in Google Calendar.

**Arguments:**
- `calendar_id` (str): Calendar ID.
- `event_id` (str): ID of the event to update.
- `summary` (str, optional): New event title.
- `start_time` (str, optional): New ISO 8601 start datetime.
- `end_time` (str, optional): New ISO 8601 end datetime.
- `description` (str, optional): New description.
- `attendees` (list of str, optional): New list of attendee emails.

**Returns:**
- The updated event object.

**Example:**
```python
update_event(calendar_id="primary", event_id="abc123", summary="Updated Meeting")
```

---

## delete_event
**Purpose:** Delete an event from Google Calendar.

**Arguments:**
- `calendar_id` (str): Calendar ID.
- `event_id` (str): Event ID to delete.

**Returns:**
- Dict with `success: True` if deleted, or error message.

**Example:**
```python
delete_event(calendar_id="primary", event_id="abc123")
```

---

## get_event_details
**Purpose:** Get details of a specific event from Google Calendar.

**Arguments:**
- `calendar_id` (str): Calendar ID.
- `event_id` (str): Event ID.

**Returns:**
- Event object dict or error.

**Example:**
```python
get_event_details(calendar_id="primary", event_id="abc123")
```

---

**Note:** All tools require a valid, authenticated Google Calendar API service object, typically handled by the agent's OAuth2 workflow.
