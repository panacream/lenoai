import os
import time
import jwt  # pyjwt

import requests
from typing import Dict, Any, List, Optional

COINBASE_API_URL = "https://api.coinbase.com/api/v3/brokerage"

CDP_AUDIENCE = "cdp.cloud.coinbase.com"

# Helper: Generate JWT for Coinbase CDP API
def _generate_coinbase_jwt() -> str:
    api_key = os.environ["COINBASE_API_KEY"]
    api_secret = os.environ["COINBASE_API_SECRET"]
    # Convert escaped newlines to real newlines if needed
    if "\\n" in api_secret:
        api_secret = api_secret.replace("\\n", "\n")
    now = int(time.time())
    payload = {
        "iss": api_key,
        "sub": api_key,
        "aud": CDP_AUDIENCE,
        "iat": now,
        "exp": now + 120,
        "nbf": now
    }
    token = jwt.encode(payload, api_secret, algorithm="ES256")
    if isinstance(token, bytes):
        token = token.decode("utf-8")
    return token

# Helper: Standard headers for all requests
def _coinbase_auth_headers() -> dict:
    return {
        "Authorization": f"Bearer {_generate_coinbase_jwt()}",
        "Content-Type": "application/json"
    }


# Helper to create request headers for Coinbase Advanced Trade API


# 1. Get all trading accounts

def get_accounts() -> List[Dict[str, Any]]:
    """
    List all trading accounts (wallets) on Coinbase.
    Returns: List of account dicts.
    """
    path = "/accounts"
    url = COINBASE_API_URL + path
    headers = _coinbase_auth_headers()
    resp = requests.get(url, headers=headers)
    resp.raise_for_status()
    return resp.json().get("accounts", [])

# 2. Get balances for a specific account

def get_account_balance(account_uuid: str) -> Dict[str, Any]:
    """
    Get balance for a specific account (by UUID).
    Args:
        account_uuid: The account UUID.
    Returns: Account balance dict.
    """
    path = f"/accounts/{account_uuid}"
    url = COINBASE_API_URL + path
    headers = _coinbase_auth_headers()
    resp = requests.get(url, headers=headers)
    resp.raise_for_status()
    return resp.json()

# 3. List products (markets)

def get_products() -> List[Dict[str, Any]]:
    """
    List all available trading products (markets), e.g., BTC-USD.
    Returns: List of product dicts.
    """
    path = "/products"
    url = COINBASE_API_URL + path
    headers = _coinbase_auth_headers()
    resp = requests.get(url, headers=headers)
    resp.raise_for_status()
    return resp.json().get("products", [])

# 4. Get ticker for a product

def get_product_ticker(product_id: str) -> Dict[str, Any]:
    """
    Get market ticker for a product (e.g., BTC-USD).
    Args:
        product_id: The product ID (e.g., 'BTC-USD').
    Returns: Ticker dict.
    """
    path = f"/products/{product_id}/ticker"
    url = COINBASE_API_URL + path
    headers = _coinbase_auth_headers()
    resp = requests.get(url, headers=headers)
    resp.raise_for_status()
    return resp.json()

# 5. Place an order

def place_order(product_id: str, side: str, size: str, order_type: str = "market", price: Optional[str] = None) -> Dict[str, Any]:
    """
    Place a trade order (buy/sell) on Coinbase Advanced Trade.
    Args:
        product_id: Product ID (e.g., 'BTC-USD').
        side: 'BUY' or 'SELL'.
        size: Amount to buy/sell (as string).
        order_type: 'market' or 'limit'.
        price: Price for limit orders.
    Returns: Order confirmation dict.
    """
    path = "/orders"
    url = COINBASE_API_URL + path
    body = {
        "product_id": product_id,
        "side": side.upper(),
        "size": size,
        "order_type": order_type.upper(),
    }
    if order_type == "limit" and price:
        body["price"] = price
    import json as _json
    body_str = _json.dumps(body)
    headers = _coinbase_auth_headers()
    resp = requests.post(url, headers=headers, data=body_str)
    resp.raise_for_status()
    return resp.json()

# 6. Get order status

def get_order_status(order_id: str) -> Dict[str, Any]:
    """
    Get the status of an order by order_id.
    Args:
        order_id: The order ID.
    Returns: Order status dict.
    """
    path = f"/orders/{order_id}"
    url = COINBASE_API_URL + path
    headers = _coinbase_auth_headers()
    resp = requests.get(url, headers=headers)
    resp.raise_for_status()
    return resp.json()

# 7. Cancel an order

def cancel_order(order_id: str) -> Dict[str, Any]:
    """
    Cancel an open order by order_id.
    Args:
        order_id: The order ID.
    Returns: Cancel confirmation dict.
    """
    path = f"/orders/{order_id}"
    url = COINBASE_API_URL + path
    headers = _coinbase_auth_headers()
    resp = requests.delete(url, headers=headers)
    resp.raise_for_status()
    return resp.json()
