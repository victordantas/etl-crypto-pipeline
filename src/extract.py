import requests

from tenacity import retry, stop_after_attempt, wait_exponential, retry_if_exception_type
from utils.logger import get_logger

logger = get_logger("extract")

API_URL = "https://api.coingecko.com/api/v3/coins/markets"

class ApiError(Exception): pass

@retry(stop=stop_after_attempt(5), wait=wait_exponential(multiplier=1, min=1, max=10),
       retry=retry_if_exception_type((requests.RequestException, ApiError)))

def fetch_market(coins: list[str], vs_currency: str = "usd") -> list[dict]:
    params = {
        "vs_currency": vs_currency,
        "ids": ",".join(coins),
        "order": "market_cap_desc",
        "per_page": len(coins),
        "page": 1,
        "sparkline": "false"
    }
    logger.info(f"Requesting {API_URL} for {coins} in {vs_currency}")
    r = requests.get(API_URL, params=params, timeout=20)
    if r.status_code != 200:
        raise ApiError(f"Non-200 status: {r.status_code} - {r.text[:200]}")
    data = r.json()
    if not isinstance(data, list):
        raise ApiError("Unexpected response format")
    logger.info(f"Fetched {len(data)} records")
    return data