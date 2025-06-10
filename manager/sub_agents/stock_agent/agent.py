from google.adk.agents.llm_agent import LlmAgent
from .tools.stock_tools import (
    get_realtime_quote,
    get_historical_data,
    place_market_order,
    get_portfolio,
    advise_diversification,
    get_latest_news
)
from .utils.instructions_loader import load_instructions_from_file
from google.adk.sessions import InMemorySessionService
from google.adk.artifacts import InMemoryArtifactService
from google.adk.runners import Runner
from dotenv import load_dotenv
import os

load_dotenv(os.path.join(os.path.dirname(__file__), "../../../.env"))

# Session and artifact service setup
artifact_service = InMemoryArtifactService()
session_service = InMemorySessionService()

# Runner
runner = Runner(
    agent=None,  # Will be set after manager_agent is instantiated
    app_name="stock_agent",
    session_service=session_service
)

# Stock Agent

stock_agent = LlmAgent(
    name="stock_agent",
    model="gemini-2.0-flash",
    description="Handles stock trading operations with the Alpaca API.",
    instruction=load_instructions_from_file("STOCK_AGENT_INSTRUCTIONS.md"),
    tools=[
        get_realtime_quote,
        get_historical_data,
        place_market_order,
        get_portfolio,
        advise_diversification,
        get_latest_news
    ],
)