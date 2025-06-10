from fastapi import APIRouter, Query
from manager.sub_agents.stock_agent.tools.stock_tools import get_realtime_quote

router = APIRouter()

@router.get("/quote")
def realtime_quote(symbol: str = Query(..., description="Stock symbol, e.g. AAPL")):
    """
    Get a real-time quote for a given stock symbol.
    """
    return get_realtime_quote(symbol)
