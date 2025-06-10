import os
import requests
from typing import Dict, Any, Optional

# LinkedIn API base URL
LINKEDIN_API_BASE = "https://api.linkedin.com/v2"

# Helper to get OAuth token from environment
def get_access_token() -> str:
    return os.getenv("LINKEDIN_ACCESS_TOKEN", "")

# 1. openid/profile/email: Fetch basic profile and email

def get_profile() -> Dict[str, Any]:
    """Fetch the authenticated user's name and photo."""
    access_token = get_access_token()
    headers = {"Authorization": f"Bearer {access_token}"}
    profile = requests.get(f"{LINKEDIN_API_BASE}/me", headers=headers).json()
    return profile

def get_email() -> Optional[str]:
    """Fetch the authenticated user's primary email address."""
    access_token = get_access_token()
    headers = {"Authorization": f"Bearer {access_token}"}
    resp = requests.get(f"{LINKEDIN_API_BASE}/emailAddress?q=members&projection=(elements*(handle~))", headers=headers).json()
    try:
        return resp['elements'][0]['handle~']['emailAddress']
    except (KeyError, IndexError):
        return None

# 2. w_member_social: Social actions (posts, comments, reactions)

def create_post(text: str, visibility: str = "PUBLIC") -> Dict[str, Any]:
    """Create a new post on behalf of the authenticated user."""
    access_token = get_access_token()
    headers = {"Authorization": f"Bearer {access_token}", "Content-Type": "application/json"}
    urn = get_profile().get("id")
    payload = {
        "author": f"urn:li:person:{urn}",
        "lifecycleState": "PUBLISHED",
        "specificContent": {
            "com.linkedin.ugc.ShareContent": {
                "shareCommentary": {"text": text},
                "shareMediaCategory": "NONE"
            }
        },
        "visibility": {"com.linkedin.ugc.MemberNetworkVisibility": visibility}
    }
    resp = requests.post(f"{LINKEDIN_API_BASE}/ugcPosts", headers=headers, json=payload)
    return resp.json()

def delete_post(post_urn: str) -> bool:
    """Delete a post by its URN. (LinkedIn API may have restrictions)"""
    # Placeholder: LinkedIn restricts post deletion via API for most apps
    return False

# 3. r_events/rw_events: Organization events

def get_organization_events(org_urn: str) -> Dict[str, Any]:
    """Retrieve your organization's events."""
    access_token = get_access_token()
    headers = {"Authorization": f"Bearer {access_token}"}
    resp = requests.get(f"{LINKEDIN_API_BASE}/events?q=organization&organization={org_urn}", headers=headers)
    return resp.json()

def create_event(org_urn: str, event_data: Dict[str, Any]) -> Dict[str, Any]:
    """Create a new event for your organization."""
    access_token = get_access_token()
    headers = {"Authorization": f"Bearer {access_token}", "Content-Type": "application/json"}
    payload = {"organization": org_urn, **event_data}
    resp = requests.post(f"{LINKEDIN_API_BASE}/events", headers=headers, json=payload)
    return resp.json()

def update_event(event_urn: str, event_data: Dict[str, Any]) -> Dict[str, Any]:
    """Update an existing organization event."""
    access_token = get_access_token()
    headers = {"Authorization": f"Bearer {access_token}", "Content-Type": "application/json"}
    resp = requests.patch(f"{LINKEDIN_API_BASE}/events/{event_urn}", headers=headers, json=event_data)
    return resp.json()

def delete_event(event_urn: str) -> bool:
    """Delete an organization event."""
    access_token = get_access_token()
    headers = {"Authorization": f"Bearer {access_token}"}
    resp = requests.delete(f"{LINKEDIN_API_BASE}/events/{event_urn}", headers=headers)
    return resp.status_code == 204

# Additional helpers for comments, reactions, etc. can be added here as needed.

# Note: All API calls should handle errors and rate limits in production code.
