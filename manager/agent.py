from google.adk.agents.llm_agent import LlmAgent
from dotenv import load_dotenv
from manager.sub_agents.coding_agent.agent import coding_agent
from manager.sub_agents.google_agent.agent import google_agent
from manager.sub_agents.scraper_agent.agent import scraper_agent
from manager.sub_agents.socialmedia_agent.agent import socialmedia_agent
from manager.sub_agents.coinbase_agent.agent import coinbase_agent
from manager.sub_agents.stock_agent.agent import stock_agent
from google.adk.sessions import InMemorySessionService
from google.adk.artifacts import InMemoryArtifactService
from google.adk.runners import Runner
from manager.tools.custom_search_tool import google_custom_search
from manager.utils.instructions_loader import load_instructions_from_file
from manager.utils.file_summarizer import summarize_file

load_dotenv(".env")

# Session and artifact service setup
artifact_service = InMemoryArtifactService()
session_service = InMemorySessionService()

# Instantiate the manager agent as the root agent
# Tool for file summarization to be callable by the agent

def summarize_txt_file(file_name: str, max_lines: int = 60) -> dict:
    """
    Summarizes the specified .txt file from the manager/docs directory.
    Args:
        file_name (str): Name of the .txt file (e.g., 'adk.txt')
        max_lines (int): Number of lines to include in the summary
    Returns:
        dict: {"status": "success", "summary": ...} or {"status": "error", "message": ...}
    """
    import os
    docs_dir = os.path.join(os.path.dirname(__file__), 'docs')
    file_path = os.path.join(docs_dir, file_name)
    summary = summarize_file(file_path, max_lines=max_lines)
    if summary.startswith("File not found") or summary.startswith("Error"):
        return {"status": "error", "message": summary}
    return {"status": "success", "summary": summary}

from google.adk.sessions import InMemorySessionService
from google.adk.runners import Runner

# Session and runner setup for agent interaction
session_service = InMemorySessionService()
APP_NAME = "agent4_app"
USER_ID = "user_1"
SESSION_ID = "session_001"

runner = Runner(
    agent=None,  # Will be set after manager_agent is instantiated
    app_name=APP_NAME,
    session_service=session_service
)

class ManagerAgent(LlmAgent):
    def handle_message(self, message):
        from google.genai.types import Content, Part
        # Always create (or overwrite) the session before running the agent
        # Always create (or overwrite) the manager session before running the agent
        session_service.create_session(app_name=APP_NAME, user_id=USER_ID, session_id=SESSION_ID)
        # Robust routing: check for pending stock trade
        stock_session = session_service.get_session(app_name="stock_agent", user_id=USER_ID, session_id=SESSION_ID)
        if stock_session and stock_session.state.get("pending_trade_action"):
            print("[ManagerAgent] Routing to stock_agent due to pending_trade_action.")
            return stock_agent.handle_message(message, user_id=USER_ID, session_id=SESSION_ID)
        msg = Content(role="user", parts=[Part(text=message)])
        result_gen = runner.run(
            user_id=USER_ID,
            session_id=SESSION_ID,
            new_message=msg
        )
        last_result = None
        for result in result_gen:
            last_result = result
        if last_result is None:
            print("[ManagerAgent] ERROR: No result produced by runner.")
            return "[ERROR] No response generated. Please try again."
        return last_result.content.parts[0].text

manager_agent = ManagerAgent(
    name="manager_agent",
    model="gemini-2.0-flash",
    description="Handles high-level management and orchestration of sub-agents.",
    instruction=load_instructions_from_file("MANAGER_AGENT_INSTRUCTIONS.md"),
    sub_agents=[google_agent, scraper_agent, coding_agent, socialmedia_agent, coinbase_agent, stock_agent],
    tools=[google_custom_search, summarize_txt_file]
)


# Now that manager_agent is set, update runner.agent
runner.agent = manager_agent

# Set the root agent
root_agent = manager_agent
