import requests
import time

BASE_URL = "https://api.kraken.com/0/public/OHLC"

INTERVAL_MAP = {
    "1m": 1, "5m": 5, "15m": 15, "1h": 60
}

def get_klines(symbol: str, interval: str, limit: int = 100):
    kraken_symbol = symbol.replace("USDT", "USD").upper()  # Basic conversion
    interval_minutes = INTERVAL_MAP.get(interval)
    if interval_minutes is None:
        raise ValueError(f"Unsupported interval for Kraken: {interval}")

    params = {
        "pair": kraken_symbol,
        "interval": interval_minutes
    }
    response = requests.get(BASE_URL, params=params)
    response.raise_for_status()
    data = response.json()

    # Format: [[time, open, high, low, close, vwap, volume, count], ...]
    pair_key = list(data['result'].keys())[0]
    candles = data['result'][pair_key]

    # Kraken returns oldest first
    return [[float(c[0]), float(c[1]), float(c[2]), float(c[3]), float(c[4]), float(c[6])] for c in candles[-limit:]]
