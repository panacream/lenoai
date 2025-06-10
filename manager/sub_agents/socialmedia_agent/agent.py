from google.adk.agents import LlmAgent
from dotenv import load_dotenv
from .sub_agents.linkedin_agent.agent import linkedin_agent
from .utils.instructions_loader import load_instructions_from_file

load_dotenv("../../../.env")

socialmedia_agent = LlmAgent(
    name="socialmedia_agent",
    model="gemini-2.0-flash",
    description="Handles social media operations, including LinkedIn interactions.",
    instruction=load_instructions_from_file("SOCIALMEDIA_AGENT_INSTRUCTIONS.md"),
    sub_agents=[linkedin_agent]
)