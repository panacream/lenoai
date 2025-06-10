# LinkedIn Agent Instructions

## Overview
The `linkedin_agent` is responsible for handling all LinkedIn-related operations delegated by the socialmedia agent. It provides a secure and reliable interface for interacting with the LinkedIn API, automating tasks such as posting, profile retrieval, and organization event management using OAuth 2.0 permissions.

## When to Use the LinkedIn Agent
The socialmedia agent should delegate to the `linkedin_agent` whenever the user requests any of the following:
- Retrieving LinkedIn profile or email information
- Creating posts or updates on LinkedIn
- Managing (fetching, creating, updating, deleting) organization events
- Any other LinkedIn-specific social or organizational actions covered by the available OAuth scopes

## Supported Actions
- **get_profile**: Fetch the authenticated user's LinkedIn profile (name, photo, etc.)
- **get_email**: Get the primary email address associated with the user's LinkedIn account
- **create_post**: Create a new post/update on behalf of the authenticated user
- **delete_post**: (Limited/placeholder) Attempt to delete a post by URN (subject to LinkedIn API restrictions)
- **get_organization_events**: Retrieve events for a specified organization
- **create_event**: Create a new event for an organization
- **update_event**: Update an existing organization event
- **delete_event**: Delete an organization event

## Integration Points
- Integrates with the LinkedIn v2 REST API
- Requires a valid OAuth 2.0 access token with the following scopes:
  - `openid`, `profile`, `email` (for user info)
  - `w_member_social` (for posting, commenting, reacting)
  - `r_events`, `rw_events` (for organization event management)
- All API calls are made using the access token stored in the environment variable

## Security and Configuration
- **LINKEDIN_ACCESS_TOKEN** must be set in the environment for API access
- Never expose access tokens in logs or user interfaces
- Handle API rate limits and errors gracefully (implement error handling in production)

## Usage Examples
- "Show my LinkedIn profile."
- "Get my LinkedIn email address."
- "Post: 'Excited to announce our new product!'"
- "Show all events for organization urn:li:organization:123456."
- "Create a LinkedIn event for our organization."
- "Update the details of event urn:li:event:7890."
- "Delete the event urn:li:event:7890."

---

**Note:**
- Some LinkedIn API features (such as post deletion) may be restricted or unavailable for most applications.
- Always ensure the access token is valid and has the required scopes before making requests.
- For organization-level actions, the authenticated user must have appropriate admin permissions on the LinkedIn organization.
