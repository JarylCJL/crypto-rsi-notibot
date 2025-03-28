# utils.py

VALID_BASE_SYMBOLS = ["BTC", "ETH", "XRP", "SOL", "BNB", "ADA", "DOGE", "DOT", "SUI"]

def normalize_symbol(input_symbol: str) -> str:
    input_symbol = input_symbol.upper()

    # Default to pairing with USDT if not already
    if not input_symbol.endswith("USDT"):
        input_symbol += "USDT"

    return input_symbol

def is_valid_symbol(symbol: str) -> bool:
    base = symbol.replace("USDT", "")
    return base in VALID_BASE_SYMBOLS
