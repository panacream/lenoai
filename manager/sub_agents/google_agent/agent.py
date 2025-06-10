from google.adk.agents.llm_agent import LlmAgent
from dotenv import load_dotenv
from .tools.gmail_tools import send_gmail, get_recent_emails, get_unread_emails, delete_email, reply_to_email, get_many_emails
from .tools.sheets_tools import read_sheet, write_sheet, append_sheet, list_sheets, describe_sheet, extract_and_log_order_receipts
from .tools.youtube_tools import (
    youtube_search_afc, youtube_get_channel_info_afc, youtube_list_playlists_afc, youtube_upload_video_afc, youtube_update_video_afc, youtube_delete_video_afc, youtube_comment_video_afc, youtube_rate_video_afc, youtube_subscribe_channel_afc, youtube_unsubscribe_channel_afc,
    youtube_comment_video_by_name_afc, youtube_rate_video_by_name_afc, youtube_update_video_by_name_afc, youtube_delete_video_by_name_afc, youtube_subscribe_channel_by_name_afc, youtube_get_channel_info_by_name_afc, youtube_list_playlists_by_channel_name_afc, youtube_get_playlist_id_by_title_afc
)
from .tools.calendar_tools import (
    list_upcoming_events, create_event, update_event, delete_event, get_event_details
)
from .utils.instructions_loader import load_instructions_from_file


load_dotenv("../.env")

# --- Register the Google Agent ---
google_agent = LlmAgent(
    name="google_agent",
    model="gemini-2.0-flash",
    description="Automates Gmail, Google Sheets, Calendar, YouTube, and Tasks for messaging, data, scheduling, and media workflows.",
    # Load both Google Agent and YouTube tool instructions
    instruction=(
        load_instructions_from_file("GOOGLE_AGENT_INSTRUCTIONS.md") + "\n\n" +
        load_instructions_from_file("YOUTUBE_TOOL_INSTRUCTIONS.md") + "\n\n" +
        load_instructions_from_file("CALENDAR_TOOL_INSTRUCTIONS.md")
    ),
    tools=[
        send_gmail, get_recent_emails, get_unread_emails, delete_email, reply_to_email, get_many_emails,
        read_sheet, write_sheet, append_sheet, list_sheets, describe_sheet, extract_and_log_order_receipts,
        youtube_search_afc, youtube_get_channel_info_afc, youtube_list_playlists_afc, youtube_upload_video_afc, youtube_update_video_afc, youtube_delete_video_afc, youtube_comment_video_afc, youtube_rate_video_afc, youtube_subscribe_channel_afc, youtube_unsubscribe_channel_afc,
        youtube_comment_video_by_name_afc, youtube_rate_video_by_name_afc, youtube_update_video_by_name_afc, youtube_delete_video_by_name_afc, youtube_subscribe_channel_by_name_afc, youtube_get_channel_info_by_name_afc, youtube_list_playlists_by_channel_name_afc, youtube_get_playlist_id_by_title_afc,
        list_upcoming_events, create_event, update_event, delete_event, get_event_details
    ],
)

# --- Shared Session State Example for Sub-Agents ---
def handle_google_task(task, session):
    """
    Example function for the google_agent to demonstrate reading/writing shared session state.
    All sub-agents should follow this pattern to access shared memory.
    """
    # Read from shared session state
    last_user_request = session.state.get('last_user_request')
    # Log this agent's last task
    session.state['google_agent_last_task'] = task
    # Optionally, append to a shared actions log
    session.state.setdefault('actions', []).append({
        'agent': 'google_agent',
        'task': task
    })
    # Return something for demonstration
    return {
        'last_user_request': last_user_request,
        'google_agent_last_task': task,
        'all_actions': session.state['actions']
    }

# Document for other sub-agents: Accept `session` as an argument, use session.state for shared memory.