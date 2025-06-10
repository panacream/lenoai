# Coinbase Agent Instructions

## Overview

The Coinbase Agent enables automated and programmatic trading on Coinbase Advanced Trade via the official API. It can retrieve account information, fetch market data, and place, check, or cancel orders on your behalf.

**Authentication:**  
This agent requires your Coinbase API Key and Secret, provided via environment variables (`COINBASE_API_KEY`, `COINBASE_API_SECRET`).  
**Never share these credentials.**

---

## Available Tools

### 1. [get_accounts](manager/sub_agents/coinbase_agent/tools/coinbase_tools.py:29:0-39:42)
**Description:**  
List all trading accounts (wallets) on your Coinbase account.

**Arguments:**  
_None_

**Returns:**  
A list of account objects, each with account UUID, currency, balance, and more.

---

### 2. [get_account_balance](manager/sub_agents/coinbase_agent/tools/coinbase_tools.py:43:0-55:22)
**Description:**  
Get the balance for a specific account.

**Arguments:**  
- `account_uuid` (string): The UUID of the account.

**Returns:**  
A dict with account balance and details.

---

### 3. [get_products](manager/sub_agents/coinbase_agent/tools/coinbase_tools.py:59:0-69:42)
**Description:**  
List all available trading products (markets), e.g., BTC-USD, ETH-USD.

**Arguments:**  
_None_

**Returns:**  
A list of product dicts with product IDs, base/quote currencies, and more.

---

### 4. [get_product_ticker](manager/sub_agents/coinbase_agent/tools/coinbase_tools.py:73:0-85:22)
**Description:**  
Get the current market ticker (price, bid/ask, etc.) for a product.

**Arguments:**  
- `product_id` (string): The product ID (e.g., 'BTC-USD').

**Returns:**  
A dict with price, bid, ask, and other market data.

---

### 5. [place_order](manager/sub_agents/coinbase_agent/tools/coinbase_tools.py:89:0-115:22)
**Description:**  
Place a buy or sell order (market or limit) on a product.

**Arguments:**  
- `product_id` (string): The product ID (e.g., 'BTC-USD').
- `side` (string): 'BUY' or 'SELL'.
- `size` (string): The amount to buy or sell.
- `order_type` (string, optional): 'market' (default) or 'limit'.
- `price` (string, optional): Required for limit orders.

**Returns:**  
A dict with order confirmation and details.

---

### 6. [get_order_status](manager/sub_agents/coinbase_agent/tools/coinbase_tools.py:119:0-131:22)
**Description:**  
Check the status of an order by its order ID.

**Arguments:**  
- `order_id` (string): The order ID.

**Returns:**  
A dict with order status and details.

---

### 7. [cancel_order](manager/sub_agents/coinbase_agent/tools/coinbase_tools.py:135:0-147:22)
**Description:**  
Cancel an open order by its order ID.

**Arguments:**  
- `order_id` (string): The order ID.

**Returns:**  
A dict confirming cancellation.

---

## Usage Examples

### List all accounts
```python
get_accounts()