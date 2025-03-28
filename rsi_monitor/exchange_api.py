from rsi_monitor.config import EXCHANGE

if EXCHANGE == "binance":
    from rsi_monitor.exchanges.binance import get_klines
elif EXCHANGE == "kraken":
    from rsi_monitor.exchanges.kraken import get_klines
else:
    raise ValueError(f"Unsupported exchange: {EXCHANGE}")
