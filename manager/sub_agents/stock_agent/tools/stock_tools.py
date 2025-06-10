"""
Stock Agent Tools
Implements trading, quote, portfolio, and news tools for the Stock Agent.
"""
import os
from typing import Optional

# TODO: Uncomment these when ready to integrate with real APIs
# from alpaca_trade_api.rest import REST, TimeFrame
# import yfinance as yf
# from datetime import datetime, timedelta

# --- API Client Setup (Alpaca, etc.) ---
# ALPACA_API_KEY = os.getenv("ALPACA_API_KEY")
# ALPACA_API_SECRET = os.getenv("ALPACA_API_SECRET")
# ALPACA_BASE_URL = os.getenv("ALPACA_BASE_URL", "https://paper-api.alpaca.markets")
# alpaca = REST(ALPACA_API_KEY, ALPACA_API_SECRET, base_url=ALPACA_BASE_URL)

# --- Tool Functions ---
def get_realtime_quote(symbol: str) -> dict:
    """
    Fetch the latest real-time quote for a stock symbol using Alpaca API.
    Returns a dictionary with quote details or an error message.
    """
    try:
        from alpaca_trade_api.rest import REST
    except ImportError:
        return {"error": "alpaca-trade-api is not installed. Please install it in your environment."}

    ALPACA_API_KEY = os.getenv("ALPACA_API_KEY")
    ALPACA_API_SECRET = os.getenv("ALPACA_API_SECRET")
    ALPACA_BASE_URL = os.getenv("ALPACA_BASE_URL", "https://paper-api.alpaca.markets")

    if not ALPACA_API_KEY or not ALPACA_API_SECRET:
        return {"error": "Alpaca API credentials are not set in environment variables."}

    try:
        alpaca = REST(ALPACA_API_KEY, ALPACA_API_SECRET, base_url=ALPACA_BASE_URL)
        quote = alpaca.get_latest_quote(symbol)
        # Defensive: handle both dict-style and attribute-style access
        symbol_val = quote.get('symbol') if hasattr(quote, 'get') else getattr(quote, 'symbol', None)
        ask_price = quote.get('ask_price') if hasattr(quote, 'get') else getattr(quote, 'ask_price', None)
        bid_price = quote.get('bid_price') if hasattr(quote, 'get') else getattr(quote, 'bid_price', None)
        ask_size = quote.get('ask_size') if hasattr(quote, 'get') else getattr(quote, 'ask_size', None)
        bid_size = quote.get('bid_size') if hasattr(quote, 'get') else getattr(quote, 'bid_size', None)
        timestamp = quote.get('timestamp') if hasattr(quote, 'get') else getattr(quote, 'timestamp', None)
        if not symbol_val or ask_price is None or bid_price is None:
            return {"error": f"Malformed quote data for {symbol}."}
        return {
            "symbol": symbol_val,
            "ask_price": ask_price,
            "bid_price": bid_price,
            "ask_size": ask_size,
            "bid_size": bid_size,
            "timestamp": str(timestamp) if timestamp is not None else None
        }
    except Exception as e:
        return {"error": f"Failed to fetch real-time quote for {symbol}: {e}"}


def get_historical_data(symbol: str, days: int = 30, timeframe: str = "1Day") -> dict:
    """
    Fetch historical OHLCV data for a symbol over the past N days.
    TODO: Integrate with Alpaca or yfinance.
    """
    return {
        "symbol": symbol.upper(),
        "data": [],
        "note": "TODO: Implement historical data fetch."
    }

def place_market_order(symbol: str, qty: int, side: str = "buy") -> dict:
    """
    Place a market order (buy/sell) for a given symbol and quantity.
    TODO: Integrate with Alpaca trading API.
    """
    return {
        "symbol": symbol.upper(),
        "qty": qty,
        "side": side,
        "status": "pending",
        "note": "TODO: Implement order placement."
    }

def get_portfolio(user_id: Optional[str] = None) -> dict:
    """
    Retrieve the user's portfolio holdings.
    TODO: Integrate with brokerage or portfolio API.
    """
    return {
        "holdings": [],
        "note": "TODO: Implement portfolio retrieval."
    }

def advise_diversification(user_id: Optional[str] = None) -> dict:
    """
    Analyze the portfolio and suggest diversification strategies.
    TODO: Implement portfolio analysis logic.
    """
    return {
        "advice": "TODO: Implement diversification advice.",
        "note": "No analysis performed."
    }

def get_latest_news(symbol: str, count: int = 5) -> dict:
    """
    Fetch the latest news headlines for a given stock symbol.
    TODO: Integrate with yfinance or news API.
    """
    return {
        "symbol": symbol.upper(),
        "news": [],
        "note": "TODO: Implement news fetch."
    }
