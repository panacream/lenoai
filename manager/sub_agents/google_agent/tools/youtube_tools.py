import os
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build

# Helper to get an authenticated YouTube API client

def get_token_path():
    # Prefer environment variable if set
    token_path = os.environ.get("YOUTUBE_TOKEN_PATH")
    print(f"Checking YOUTUBE_TOKEN_PATH: {token_path}")
    if token_path and os.path.exists(token_path):
        print(f"Found token at YOUTUBE_TOKEN_PATH: {token_path}")
        return token_path
    # Default to project root
    project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../../../'))
    default_path = os.path.join(project_root, "token.json")
    print(f"Checking default path: {default_path}, exists: {os.path.exists(default_path)}")
    if os.path.exists(default_path):
        print(f"Found token at default path: {default_path}")
        return default_path
    raise FileNotFoundError("token.json not found in project root or YOUTUBE_TOKEN_PATH not set.")

def get_youtube_service():
    creds = Credentials.from_authorized_user_file(
        get_token_path(),
        ["https://www.googleapis.com/auth/youtube", "https://www.googleapis.com/auth/youtube.force-ssl"]
    )
    return build("youtube", "v3", credentials=creds)

# 1. Search videos
# AFC-compatible wrappers for all YouTube tools

def youtube_search_afc(query: str, max_results: int):
    """
    AFC-compatible: Search for YouTube videos by keyword.
    """
    return youtube_search(query, max_results)

def youtube_get_channel_info_afc(channel_id: str):
    """
    AFC-compatible: Get information about a YouTube channel.
    """
    return youtube_get_channel_info(channel_id)

def youtube_list_playlists_afc(channel_id: str, max_results: int):
    """
    AFC-compatible: List playlists for a channel.
    """
    return youtube_list_playlists(channel_id, max_results)

# Original implementation (keep for internal use, not for AFC)
def youtube_search(query, max_results=5):
    service = get_youtube_service()
    request = service.search().list(q=query, part='snippet', type='video', maxResults=max_results)
    response = request.execute()
    return [{
        'title': item['snippet']['title'],
        'videoId': item['id']['videoId'],
        'channelTitle': item['snippet']['channelTitle']
    } for item in response.get('items', [])]

def youtube_get_channel_info(channel_id):
    service = get_youtube_service()
    request = service.channels().list(part='snippet,statistics', id=channel_id)
    response = request.execute()
    if response['items']:
        return response['items'][0]
    return {'error': 'Channel not found.'}

def youtube_list_playlists(channel_id, max_results=10):
    service = get_youtube_service()
    request = service.playlists().list(part='snippet', channelId=channel_id, maxResults=max_results)
    response = request.execute()
    return [{
        'playlistId': item['id'],
        'title': item['snippet']['title'],
        'description': item['snippet']['description']
    } for item in response.get('items', [])]

# --- Helper functions to find IDs by name/title ---

def find_video_id_by_title(title: str, max_results: int = 10):
    """Return the videoId of the first video matching the given title (case-insensitive)."""
    results = youtube_search(title, max_results)
    for v in results:
        if v['title'].strip().lower() == title.strip().lower():
            return v['videoId']
    # fallback: return first result if exists
    if results:
        return results[0]['videoId']
    return None

def find_channel_id_by_name(channel_name: str, max_results: int = 10):
    """Return the channelId of the first channel matching the given name (case-insensitive)."""
    service = get_youtube_service()
    request = service.search().list(q=channel_name, part='snippet', type='channel', maxResults=max_results)
    response = request.execute()
    for item in response.get('items', []):
        if item['snippet']['channelTitle'].strip().lower() == channel_name.strip().lower():
            return item['snippet']['channelId']
    # fallback: return first result if exists
    if response.get('items', []):
        return response['items'][0]['snippet']['channelId']
    return None

def find_playlist_id_by_title(channel_id: str, playlist_title: str, max_results: int = 20):
    """Return the playlistId of the first playlist matching the given title for a channel."""
    playlists = youtube_list_playlists(channel_id, max_results)
    for p in playlists:
        if p['title'].strip().lower() == playlist_title.strip().lower():
            return p['playlistId']
    # fallback: return first result if exists
    if playlists:
        return playlists[0]['playlistId']
    return None

# --- AFC-compatible wrappers for actions by name/title ---

def youtube_comment_video_by_name_afc(video_title: str, text: str):
    """AFC: Comment on a video by its title."""
    video_id = find_video_id_by_title(video_title)
    if not video_id:
        return {'error': f'No video found with title: {video_title}'}
    return youtube_comment_video(video_id, text)

def youtube_rate_video_by_name_afc(video_title: str, rating: str):
    """AFC: Rate a video by its title ('like', 'dislike', 'none')."""
    video_id = find_video_id_by_title(video_title)
    if not video_id:
        return {'error': f'No video found with title: {video_title}'}
    return youtube_rate_video(video_id, rating)

def youtube_update_video_by_name_afc(video_title: str, new_title: str, description: str, tags: str):
    """AFC: Update video metadata by video title."""
    video_id = find_video_id_by_title(video_title)
    if not video_id:
        return {'error': f'No video found with title: {video_title}'}
    tag_list = [t.strip() for t in tags.split(",")] if tags else []
    return youtube_update_video(video_id, new_title, description, tag_list)

def youtube_delete_video_by_name_afc(video_title: str):
    """AFC: Delete a video by its title."""
    video_id = find_video_id_by_title(video_title)
    if not video_id:
        return {'error': f'No video found with title: {video_title}'}
    return youtube_delete_video(video_id)

def youtube_subscribe_channel_by_name_afc(channel_name: str):
    """AFC: Subscribe to a channel by channel name."""
    channel_id = find_channel_id_by_name(channel_name)
    if not channel_id:
        return {'error': f'No channel found with name: {channel_name}'}
    return youtube_subscribe_channel(channel_id)

def youtube_get_channel_info_by_name_afc(channel_name: str):
    """AFC: Get channel info by channel name."""
    channel_id = find_channel_id_by_name(channel_name)
    if not channel_id:
        return {'error': f'No channel found with name: {channel_name}'}
    return youtube_get_channel_info(channel_id)

def youtube_list_playlists_by_channel_name_afc(channel_name: str, max_results: int):
    """AFC: List playlists for a channel by channel name."""
    channel_id = find_channel_id_by_name(channel_name)
    if not channel_id:
        return {'error': f'No channel found with name: {channel_name}'}
    return youtube_list_playlists(channel_id, max_results)

def youtube_get_playlist_id_by_title_afc(channel_name: str, playlist_title: str):
    """AFC: Get playlist ID by channel name and playlist title."""
    channel_id = find_channel_id_by_name(channel_name)
    if not channel_id:
        return {'error': f'No channel found with name: {channel_name}'}
    playlist_id = find_playlist_id_by_title(channel_id, playlist_title)
    if not playlist_id:
        return {'error': f'No playlist found with title: {playlist_title}'}
    return {'playlistId': playlist_id}


def youtube_upload_video_afc(file_path: str, title: str, description: str, tags: str, privacy_status: str):
    """
    AFC-compatible: Upload a video to YouTube.
    tags: comma-separated string, privacy_status: 'private', 'public', or 'unlisted'
    """
    tag_list = [t.strip() for t in tags.split(",")] if tags else []
    return youtube_upload_video(file_path, title, description, tag_list, privacy_status)

def youtube_update_video_afc(video_id: str, title: str, description: str, tags: str):
    """
    AFC-compatible: Update video metadata.
    tags: comma-separated string
    """
    tag_list = [t.strip() for t in tags.split(",")] if tags else []
    return youtube_update_video(video_id, title, description, tag_list)

def youtube_delete_video_afc(video_id: str):
    """
    AFC-compatible: Delete a video by ID.
    """
    return youtube_delete_video(video_id)

def youtube_comment_video_afc(video_id: str, text: str):
    """
    AFC-compatible: Post a comment on a video.
    """
    return youtube_comment_video(video_id, text)

def youtube_rate_video_afc(video_id: str, rating: str):
    """
    AFC-compatible: Rate a video ('like', 'dislike', or 'none').
    """
    return youtube_rate_video(video_id, rating)

def youtube_subscribe_channel_afc(channel_id: str):
    """
    AFC-compatible: Subscribe to a channel.
    """
    return youtube_subscribe_channel(channel_id)

def youtube_unsubscribe_channel_afc(subscription_id: str):
    """
    AFC-compatible: Unsubscribe from a channel (requires subscription ID).
    """
    return youtube_unsubscribe_channel(subscription_id)

# Original implementations (keep for internal use, not for AFC)
def youtube_upload_video(file_path, title, description='', tags=None, privacy_status='private'):
    from googleapiclient.http import MediaFileUpload
    service = get_youtube_service()
    body = {
        'snippet': {
            'title': title,
            'description': description,
            'tags': tags or []
        },
        'status': {
            'privacyStatus': privacy_status
        }
    }
    media = MediaFileUpload(file_path, chunksize=-1, resumable=True)
    request = service.videos().insert(part='snippet,status', body=body, media_body=media)
    response = request.execute()
    return {'videoId': response['id']}

def youtube_update_video(video_id, title=None, description=None, tags=None):
    service = get_youtube_service()
    body = {'id': video_id, 'snippet': {}}
    if title: body['snippet']['title'] = title
    if description: body['snippet']['description'] = description
    if tags: body['snippet']['tags'] = tags
    body['snippet']['categoryId'] = '22'  # People & Blogs (as default)
    request = service.videos().update(part='snippet', body=body)
    response = request.execute()
    return response

def youtube_delete_video(video_id):
    service = get_youtube_service()
    service.videos().delete(id=video_id).execute()
    return {'status': 'success', 'videoId': video_id}

def youtube_comment_video(video_id, text):
    service = get_youtube_service()
    body = {
        'snippet': {
            'videoId': video_id,
            'topLevelComment': {
                'snippet': {
                    'textOriginal': text
                }
            }
        }
    }
    request = service.commentThreads().insert(part='snippet', body=body)
    response = request.execute()
    return response

def youtube_rate_video(video_id, rating):
    service = get_youtube_service()
    service.videos().rate(id=video_id, rating=rating).execute()
    return {'status': 'success', 'videoId': video_id, 'rating': rating}

def youtube_subscribe_channel(channel_id):
    service = get_youtube_service()
    body = {'snippet': {'resourceId': {'kind': 'youtube#channel', 'channelId': channel_id}}}
    request = service.subscriptions().insert(part='snippet', body=body)
    response = request.execute()
    return response

def youtube_unsubscribe_channel(subscription_id):
    service = get_youtube_service()
    service.subscriptions().delete(id=subscription_id).execute()
    return {'status': 'success', 'subscriptionId': subscription_id}
