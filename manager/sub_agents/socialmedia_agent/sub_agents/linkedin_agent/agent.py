from google.adk.agents import LlmAgent
from dotenv import load_dotenv
from .utils.instructions_loader import load_instructions_from_file
from .tools.linkedin_tools import (
    get_profile,
    get_email,
    create_post,
    delete_post,
    get_organization_events,
    create_event,
    update_event,
    delete_event
)

load_dotenv("../../../.env")

linkedin_agent = LlmAgent(
    name="linkedin_agent",
    model="gemini-1.5-pro",
    description="Handles all LinkedIn-specific social media operations, including profile retrieval, posting, and organization event management.",
    instruction=load_instructions_from_file("LINKEDIN_AGENT_INSTRUCTIONS.md"),
    tools=[
        get_profile,
        get_email,
        create_post,
        delete_post,
        get_organization_events,
        create_event,
        update_event,
        delete_event
    ]
)