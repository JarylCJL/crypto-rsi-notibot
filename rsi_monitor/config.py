# config.py

EXCHANGE = "binance"  # Options: "binance", "kraken"

# RSI thresholds to watch for
RSI_THRESHOLDS = [
    (70, 'above'), (30, 'below'),
    (75, 'above'), (25, 'below'),
    (80, 'above'), (20, 'below')
]

# Time intervals and their API keys
INTERVALS = {
    '1m': '1m',
    '5m': '5m',
    '15m': '15m',
    '1h': '1h',
    '4h': '4h',
    '1d': '1d'
}

# RSI period to use for calculations
DEFAULT_RSI_PERIOD = 14

SUPPORTED_SYMBOLS = ["BTC", "ETH", "XRP", "SOL", "BNB", "ADA", "DOGE", "DOT", "SUI", "MATIC"]

def normalize_symbol(input_symbol: str) -> str:
    input_symbol = input_symbol.upper()

    # Default to pairing with USDT if not already
    if not input_symbol.endswith("USDT"):
        input_symbol += "USDT"

    return input_symbol

def is_valid_symbol(symbol: str) -> bool:
    base = symbol.replace("USDT", "")
    return base in SUPPORTED_SYMBOLS