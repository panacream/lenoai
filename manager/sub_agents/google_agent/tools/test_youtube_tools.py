import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../../..')))
import pytest
from manager.sub_agents.google_agent.tools.youtube_tools import (
    youtube_search, youtube_get_channel_info, youtube_list_playlists, youtube_upload_video, youtube_update_video, youtube_delete_video, youtube_comment_video, youtube_rate_video, youtube_subscribe_channel, youtube_unsubscribe_channel
)

# Note: These tests require a valid token.json with correct YouTube API scopes and may perform real actions on your account.
# For upload/delete, use a small test video and a test channel if possible.

@pytest.mark.skipif(not os.path.exists(os.path.join(os.path.dirname(__file__), '../../../../token.json')), reason="No token.json found")
def test_youtube_search():
    results = youtube_search("python programming", max_results=2)
    assert isinstance(results, list)
    assert len(results) <= 2
    assert all('videoId' in v for v in results)

def test_youtube_get_channel_info():
    # Use a well-known channel ID (e.g., Google Developers)
    info = youtube_get_channel_info("UC_x5XG1OV2P6uZZ5FSM9Ttw")
    assert 'snippet' in info
    assert 'statistics' in info

def test_youtube_list_playlists():
    playlists = youtube_list_playlists("UC_x5XG1OV2P6uZZ5FSM9Ttw", max_results=2)
    assert isinstance(playlists, list)
    if playlists:
        assert 'playlistId' in playlists[0]

def test_youtube_upload_and_delete(monkeypatch):
    # Upload a small test video (must exist)
    test_video = os.path.join(os.path.dirname(__file__), 'test_video.mp4')
    if not os.path.exists(test_video):
        pytest.skip("No test_video.mp4 found for upload test.")
    upload_result = youtube_upload_video(test_video, "Test Upload", description="Test video upload.")
    assert 'videoId' in upload_result
    video_id = upload_result['videoId']
    # Now delete it
    delete_result = youtube_delete_video(video_id)
    assert delete_result['status'] == 'success'
    assert delete_result['videoId'] == video_id

def test_youtube_comment_and_rate():
    # Use a known public video
    video_id = "dQw4w9WgXcQ"
    comment_response = youtube_comment_video(video_id, "Automated test comment.")
    assert 'snippet' in comment_response['snippet']['topLevelComment']
    rate_result = youtube_rate_video(video_id, rating="like")
    assert rate_result['status'] == 'success'
    assert rate_result['videoId'] == video_id
    assert rate_result['rating'] == 'like'

def test_youtube_subscribe_and_unsubscribe():
    # Use a known channel
    channel_id = "UC_x5XG1OV2P6uZZ5FSM9Ttw"
    subscribe_response = youtube_subscribe_channel(channel_id)
    assert 'id' in subscribe_response
    subscription_id = subscribe_response['id']
    # Now unsubscribe
    unsubscribe_response = youtube_unsubscribe_channel(subscription_id)
    assert unsubscribe_response['status'] == 'success'
    assert unsubscribe_response['subscriptionId'] == subscription_id
