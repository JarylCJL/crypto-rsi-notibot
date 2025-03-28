import requests

BASE_URL = "https://api.binance.com"

def get_klines(symbol: str, interval: str, limit: int = 100):
    url = f"{BASE_URL}/api/v3/klines"
    params = {
        "symbol": symbol.upper(),
        "interval": interval,
        "limit": limit
    }
    response = requests.get(url, params=params)
    response.raise_for_status()
    return response.json()
