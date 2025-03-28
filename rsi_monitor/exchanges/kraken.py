import requests

def get_klines(symbol, interval, limit=100):
    # Normalize symbol for Kraken
    symbol_map = {
        "BTCUSDT": "XBTUSDT",
        "BTCUSD": "XBTUSD",
        "ETHUSD": "ETHUSD",
        "ETHUSDT": "ETHUSDT",
        "XRPUSDT": "XRPUSDT",
    }
    kraken_symbol = symbol_map.get(symbol.upper(), symbol.upper())

    interval_map = {
        "1m": 1,
        "5m": 5,
        "15m": 15,
        "30m": 30,
        "1h": 60,
        "4h": 240,
        "1d": 1440
    }
    kraken_interval = interval_map.get(interval, 5)

    url = "https://api.kraken.com/0/public/OHLC"
    params = {
        "pair": kraken_symbol,
        "interval": kraken_interval,
        "since": 0  # you may adjust for real-time start
    }

    response = requests.get(url, params=params)
    data = response.json()

    # Handle known Kraken errors
    if "error" in data and data["error"]:
        print(f"[KRAKEN ERROR] {kraken_symbol} ({interval}): {data['error']}")
        return []

    if "result" not in data:
        print(f"[KRAKEN] Unexpected response for {kraken_symbol}: {data}")
        return []

    # Kraken returns result as {pair_name: [[...], [...]]}
    # Extract the first value inside the result
    try:
        ohlc_data = next(iter(data["result"].values()))
        return ohlc_data[:limit]
    except Exception as e:
        print(f"[KRAKEN PARSE ERROR] {kraken_symbol}: {e}")
        return []
