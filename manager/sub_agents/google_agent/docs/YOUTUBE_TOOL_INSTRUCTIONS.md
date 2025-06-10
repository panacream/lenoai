# YouTube Tool Instructions

This document describes the YouTube-related tools available to the Google agent. Each tool is registered and can be called by the agent to interact with the YouTube API for a variety of tasks.

---

## youtube_search
**Purpose:** Search for YouTube videos by keyword.

**Arguments:**
- `query` (str): The search query.
- `max_results` (int, optional): Maximum number of results to return (default: 5).

**Returns:**
- List of videos with `title`, `videoId`, and `channelTitle`.

**Example:**
```python
youtube_search("lofi hip hop", max_results=3)
```

---

## youtube_get_channel_info
**Purpose:** Get information about a YouTube channel.

**Arguments:**
- `channel_id` (str): The channel's ID.

**Returns:**
- Channel metadata (snippet and statistics) or error if not found.

**Example:**
```python
youtube_get_channel_info("UC_x5XG1OV2P6uZZ5FSM9Ttw")
```

---

## youtube_list_playlists
**Purpose:** List playlists for a channel.

**Arguments:**
- `channel_id` (str): The channel's ID.
- `max_results` (int, optional): Maximum number of playlists (default: 10).

**Returns:**
- List of playlists with `playlistId`, `title`, `description`.

**Example:**
```python
youtube_list_playlists("UC_x5XG1OV2P6uZZ5FSM9Ttw", max_results=5)
```

---

## youtube_upload_video
**Purpose:** Upload a video to YouTube.

**Arguments:**
- `file_path` (str): Path to the video file.
- `title` (str): Video title.
- `description` (str, optional): Video description.
- `tags` (list of str, optional): Tags for the video.
- `privacy_status` (str, optional): 'private', 'public', or 'unlisted' (default: 'private').

**Returns:**
- Video ID of the uploaded video.

**Example:**
```python
youtube_upload_video("/path/to/video.mp4", "My Vlog", description="A new vlog!", tags=["vlog", "daily"], privacy_status="public")
```

---

## youtube_update_video
**Purpose:** Update video metadata.

**Arguments:**
- `video_id` (str): ID of the video to update.
- `title` (str, optional): New title.
- `description` (str, optional): New description.
- `tags` (list of str, optional): New tags.

**Returns:**
- Updated video metadata.

**Example:**
```python
youtube_update_video("dQw4w9WgXcQ", title="Updated Title", description="New description.", tags=["music", "remix"])
```

---

## youtube_delete_video
**Purpose:** Delete a video by ID.

**Arguments:**
- `video_id` (str): ID of the video to delete.

**Returns:**
- Status and video ID.

**Example:**
```python
youtube_delete_video("dQw4w9WgXcQ")
```

---

## youtube_comment_video
**Purpose:** Post a comment on a video.

**Arguments:**
- `video_id` (str): ID of the video.
- `text` (str): Comment text.

**Returns:**
- API response with comment details.

**Example:**
```python
youtube_comment_video("dQw4w9WgXcQ", "Great video!")
```

---

## youtube_rate_video
**Purpose:** Like, dislike, or remove rating from a video.

**Arguments:**
- `video_id` (str): ID of the video.
- `rating` (str): 'like', 'dislike', or 'none'.

**Returns:**
- Status, video ID, and applied rating.

**Example:**
```python
youtube_rate_video("dQw4w9WgXcQ", rating="like")
```

---

## youtube_subscribe_channel
**Purpose:** Subscribe to a channel.

**Arguments:**
- `channel_id` (str): ID of the channel to subscribe to.

**Returns:**
- API response with subscription details.

**Example:**
```python
youtube_subscribe_channel("UC_x5XG1OV2P6uZZ5FSM9Ttw")
```

---

## youtube_unsubscribe_channel
**Purpose:** Unsubscribe from a channel (requires subscription ID).

**Arguments:**
- `subscription_id` (str): ID of the subscription to remove.

**Returns:**
- Status and subscription ID.

**Example:**
```python
youtube_unsubscribe_channel("SUBSCRIPTION_ID")
```

---

**Note:** All tools require valid OAuth2 credentials and proper YouTube Data API scopes. See `token.json` and your OAuth setup for more details.
