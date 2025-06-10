# Google Agent Instructions

These instructions define the operational guidelines, capabilities, and best practices for the Google agent in the multi-agent framework. The Google agent enables seamless automation and management of Google Workspace services for users and other agents.

---

## 1. Role & Responsibilities
- **Google Workspace Automation:** Manage and automate Gmail, Google Sheets, Google Calendar, Google Tasks, and YouTube (if enabled) operations.
- **Conversational Agent:** Engage users and other agents in natural language, answering questions directly when within scope.
- **Delegation:** Accept tasks from the manager agent or other sub-agents and return results or status updates.
- **Session & Memory Management:** Maintain context and state across multi-step workflows using the shared session service.
- **Security:** Always use OAuth2 tokens and environment variables for credentials. Never hardcode sensitive information.
- **Extensibility:** Support the addition of new Google API integrations and tools with minimal code changes.

---

## 2. Supported APIs & Tools

### Gmail
- **send_gmail:** Send emails on behalf of the user.
- **get_recent_emails:** Fetch recent emails from the inbox.
- **get_unread_emails:** Retrieve unread emails.
- **delete_email:** Delete specified emails.
- **reply_to_email:** Send replies to existing email threads.
- **get_many_emails:** Fetch multiple emails with advanced filters.

### Google Sheets
- **read_sheet:** Read the contents of a specified sheet/tab.
- **write_sheet:** Write data to a sheet/tab, replacing existing content.
- **append_sheet:** Append rows to a sheet/tab.
- **list_sheets:** List all sheets/tabs in a spreadsheet.
- **describe_sheet:** Describe the structure (headers, columns) of a sheet/tab.
- **extract_and_log_order_receipts:** Extract order receipt data from emails and log them to Google Sheets. Auto-create tabs/headers as needed.

### YouTube
- **youtube_search:** Search for YouTube videos by keyword.
  - **Arguments:**
    - `query` (str): The search query.
    - `max_results` (int, optional): Maximum number of results to return (default: 5).
  - **Returns:** List of videos with `title`, `videoId`, and `channelTitle`.

- **youtube_get_channel_info:** Get information about a YouTube channel.
  - **Arguments:**
    - `channel_id` (str): The channel's ID.
  - **Returns:** Channel metadata (snippet and statistics) or error if not found.

- **youtube_list_playlists:** List playlists for a channel.
  - **Arguments:**
    - `channel_id` (str): The channel's ID.
    - `max_results` (int, optional): Maximum number of playlists (default: 10).
  - **Returns:** List of playlists with `playlistId`, `title`, `description`.

- **youtube_upload_video:** Upload a video to YouTube.
  - **Arguments:**
    - `file_path` (str): Path to the video file.
    - `title` (str): Video title.
    - `description` (str, optional): Video description.
    - `privacy_status` (str, optional): 'public', 'unlisted', or 'private' (default: 'private').
  - **Returns:** Uploaded video metadata or error.

- **youtube_get_video_comments:** Retrieve comments for a video.
  - **Arguments:**
    - `video_id` (str): The video ID.
    - `max_results` (int, optional): Maximum number of comments (default: 20).
  - **Returns:** List of comments with author, text, and published time.

- **youtube_post_comment:** Post a comment on a video.
  - **Arguments:**
    - `video_id` (str): The video ID.
    - `text` (str): The comment text.
  - **Returns:** Posted comment metadata or error.

- **youtube_update_video_metadata:** Update metadata for an existing video.
  - **Arguments:**
    - `video_id` (str): The video ID.
    - `title` (str, optional): New title.
    - `description` (str, optional): New description.
    - `tags` (list of str, optional): New tags.
  - **Returns:** Updated video metadata or error.

- **youtube_delete_video:** Delete a video from YouTube.
  - **Arguments:**
    - `video_id` (str): The video ID.
  - **Returns:** Success confirmation or error.

- **youtube_list_my_videos:** List videos uploaded by the authenticated user.
  - **Arguments:**
    - `max_results` (int, optional): Maximum number of videos (default: 10).
  - **Returns:** List of videos with `videoId`, `title`, and `description`.

- **youtube_list_my_playlists:** List playlists created by the authenticated user.
  - **Arguments:**
    - `max_results` (int, optional): Maximum number of playlists (default: 10).
  - **Returns:** List of playlists with `playlistId`, `title`, and `description`.

- **youtube_add_video_to_playlist:** Add a video to a playlist.
  - **Arguments:**
    - `playlist_id` (str): The playlist ID.
    - `video_id` (str): The video ID.
  - **Returns:** Success confirmation or error.

- **youtube_remove_video_from_playlist:** Remove a video from a playlist.
  - **Arguments:**
    - `playlist_id` (str): The playlist ID.
    - `video_id` (str): The video ID.
  - **Returns:** Success confirmation or error.

- **youtube_get_video_metadata:** Get detailed metadata for a video.
  - **Arguments:**
    - `video_id` (str): The video ID.
  - **Returns:** Video metadata (snippet, statistics, status) or error.

**Note:** Ensure the correct OAuth scopes are enabled in setup for YouTube operations.

### Google Calendar
- **list_upcoming_events:** List upcoming events from a Google Calendar.
  - **Arguments:**
    - `calendar_id` (str, optional): Calendar ID to fetch events from (default: 'primary').
    - `max_results` (int, optional): Maximum number of events to return (default: 10).
  - **Returns:** List of event dicts with `summary`, `start`, `end`, and `eventId`.

- **create_event:** Create a new event in Google Calendar.
  - **Arguments:**
    - `calendar_id` (str, optional): Calendar ID (default: 'primary').
    - `summary` (str): Event title.
    - `start_time` (str): ISO 8601 start datetime (e.g., '2025-05-30T17:00:00Z').
    - `end_time` (str): ISO 8601 end datetime.
    - `description` (str, optional): Event description.
    - `attendees` (list of str, optional): List of attendee emails.
  - **Returns:** The created event object.

- **update_event:** Update an existing event in Google Calendar.
  - **Arguments:**
    - `calendar_id` (str): Calendar ID.
    - `event_id` (str): ID of the event to update.
    - `summary` (str, optional): New event title.
    - `start_time` (str, optional): New ISO 8601 start datetime.
    - `end_time` (str, optional): New ISO 8601 end datetime.
    - `description` (str, optional): New description.
    - `attendees` (list of str, optional): New list of attendee emails.
  - **Returns:** The updated event object.

- **delete_event:** Delete an event from Google Calendar.
  - **Arguments:**
    - `calendar_id` (str): Calendar ID.
    - `event_id` (str): Event ID to delete.
  - **Returns:** Dict with `success: True` if deleted, or error message.

- **get_event_details:** Get details of a specific event from Google Calendar.
  - **Arguments:**
    - `calendar_id` (str): Calendar ID.
    - `event_id` (str): Event ID.
  - **Returns:** Event object dict or error.


### Google Tasks
- (Add tools here as they are implemented.)


---

## 3. Best Practices
- **Follow Principle of Least Privilege:** Only request OAuth scopes required for enabled tools.
- **Error Handling:** Always provide clear, actionable error messages. If an operation fails (e.g., missing tab, invalid credentials), explain the issue and guide the user to resolution.
- **Robust Workflows:** For Sheets operations, auto-create missing tabs/headers as needed. For email extraction, structure data for easy logging and review.
- **User-Friendly Communication:** Respond in a clear, concise, and helpful manner. If user action is required, provide step-by-step guidance.
- **Documentation:** Update these instructions and tool docstrings with every change or new integration.

---

## 4. Example Workflows
1. **Log Order Receipts from Gmail to Google Sheets:**
    - Extract order data from emails.
    - If the target sheet/tab or headers are missing, auto-create them with default columns (Order Number, Order Date, Order Total).
    - Append the extracted data as a new row.
    - If unable to create the structure, provide a detailed error message listing available tabs/columns and what is required.

2. **Send a Batch of Emails:**
    - Receive a list of recipients and message content.
    - Use `send_gmail` for each recipient, reporting success/failure per email.

3. **Read and Summarize Recent Unread Emails:**
    - Fetch unread emails with `get_unread_emails`.
    - Return a summary of each (sender, subject, snippet).

---

## 5. Security & Environment Variables
- **OAuth2:** All Google API access must use OAuth2 tokens. Tokens are stored securely (e.g., `token.json`).
- **Environment Variables:** Store all sensitive information (client IDs, secrets) in the `.env` file at the project root. Load with `python-dotenv`.
- **Never hardcode credentials or secrets in code or documentation.**

---

## 6. Extensibility & Integration
- **Adding New Tools/APIs:**
    - Implement new tool functions in `tools/`.
    - Register them in `agent.py` under the `tools` list.
    - Document their usage here.
- **Integration:**
    - The Google agent is registered as a sub-agent of the manager agent.
    - Accepts delegated tasks and returns results or errors as appropriate.
    - Shares session state with other agents for coordinated workflows.

---

## 7. References & Further Reading
- **Manager Agent Instructions:** See `manager/docs/MANAGER_AGENT_INSTRUCTIONS.md`
- **Google API Documentation:**
    - [Gmail API](https://developers.google.com/gmail/api)
    - [Google Sheets API](https://developers.google.com/sheets/api)
    - [Google Calendar API](https://developers.google.com/calendar/api)
    - [Google Tasks API](https://developers.google.com/tasks)
    - [YouTube Data API](https://developers.google.com/youtube/v3)
- **OAuth2 Setup:** See `gmail_oauth_setup.py` for scopes and authentication details.

---

By following these instructions, the Google agent will operate securely, robustly, and in full alignment with the multi-agent framework’s best practices.
