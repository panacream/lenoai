import os
import requests
from dotenv import load_dotenv

load_dotenv(os.path.join(os.path.dirname(__file__), '../../.env'))

CUSTOM_SEARCH_API_KEY = os.getenv('CUSTOM_SEARCH_API_KEY')


def google_custom_search(query: str, cse_id: str, num: int = 10) -> dict:
    """
    Uses Google Custom Search API to return search results for a query.
    Args:
        query (str): Search query string.
        cse_id (str): Custom Search Engine ID (cx).
        num (int): Number of results to return (max 10 per request).
    Returns:
        dict: { 'status': 'success', 'results': [ { 'title': ..., 'snippet': ..., 'link': ... }, ... ] }
              or { 'status': 'error', 'message': ... }
    """
    if not CUSTOM_SEARCH_API_KEY or not cse_id:
        return {'status': 'error', 'message': 'Missing API key or CSE ID.'}
    url = 'https://www.googleapis.com/customsearch/v1'
    params = {
        'key': CUSTOM_SEARCH_API_KEY,
        'cx': cse_id,
        'q': query,
        'num': num
    }
    try:
        resp = requests.get(url, params=params, timeout=10)
        resp.raise_for_status()
        data = resp.json()
        results = []
        for item in data.get('items', []):
            results.append({
                'title': item.get('title'),
                'snippet': item.get('snippet'),
                'link': item.get('link')
            })
        return {'status': 'success', 'results': results}
    except Exception as e:
        return {'status': 'error', 'message': str(e)}
