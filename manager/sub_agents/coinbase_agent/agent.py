from google.adk.agents.llm_agent import LlmAgent
from dotenv import load_dotenv
from .utils.instructions_loader import load_instructions_from_file

load_dotenv("../../../.env")

from .tools.coinbase_tools import (
    get_accounts,
    get_account_balance,
    get_products,
    get_product_ticker,
    place_order,
    get_order_status,
    cancel_order
)

coinbase_agent = LlmAgent(
    name="coinbase_agent",
    model="gemini-2.0-flash",
    description="Handles all Coinbase Advanced Trade operations, including account info, market data, and trading.",
    instruction=load_instructions_from_file("COINBASE_AGENT_INSTRUCTIONS.md"),
    tools=[
        get_accounts,
        get_account_balance,
        get_products,
        get_product_ticker,
        place_order,
        get_order_status,
        cancel_order
    ]
)