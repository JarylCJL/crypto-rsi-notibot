from rsi_monitor.exchange_api import get_klines
from rsi_monitor.rsi_calculator import calculate_rsi

# RSI thresholds to monitor
RSI_THRESHOLDS = [
    (70, 'above'), (30, 'below'),
    (75, 'above'), (25, 'below'),
    (80, 'above'), (20, 'below')
]

# Standard intervals (label → Binance/Kraken key)
INTERVALS = {
    '5m': '5m',
    '15m': '15m',
    '1h': '1h'
}

class RSIMonitor:
    def __init__(self, symbols):
        self.symbols = symbols
        # Track threshold state per symbol/interval/threshold
        self.last_cross = {
            symbol: {interval: {} for interval in INTERVALS}
            for symbol in symbols
        }

    def fetch_klines(self, symbol, interval, limit=100):
        """Fetch OHLCV candles for a given symbol + interval"""
        return get_klines(symbol, interval, limit)

    def compute_rsi(self, klines, period=14):
        """Compute RSI from kline closing prices"""
        closes = [float(k[4]) for k in klines]
        return calculate_rsi(closes, period=period)

    def poll(self):
        """Poll RSI values and return threshold-crossing alerts"""
        alerts = []
        for symbol in self.symbols:
            for label, interval in INTERVALS.items():
                try:
                    klines = self.fetch_klines(symbol, interval)
                    rsi_values = self.compute_rsi(klines)
                    if not rsi_values or rsi_values[-1] is None:
                        continue

                    rsi = rsi_values[-1]

                    # Always print current RSI
                    print(f"[RSI] {symbol} ({label}) → {rsi:.2f}")

                    for threshold, direction in RSI_THRESHOLDS:
                        key = f"{direction}_{threshold}"
                        prev_state = self.last_cross[symbol][label].get(key)

                        crossed = (
                            (direction == 'above' and rsi > threshold and (prev_state is None or prev_state == 'below')) or
                            (direction == 'below' and rsi < threshold and (prev_state is None or prev_state == 'above'))
                        )

                        if crossed:
                            print(f"[ALERT] {symbol} ({label}) RSI={rsi:.2f} crossed {direction.upper()} {threshold}")
                            alerts.append((symbol, label, rsi, threshold, direction))
                            self.last_cross[symbol][label][key] = direction
                        else:
                            # Reset state if RSI has reversed
                            if (direction == 'above' and rsi < threshold) or (direction == 'below' and rsi > threshold):
                                self.last_cross[symbol][label][key] = 'below' if direction == 'above' else 'above'

                except Exception as e:
                    print(f"[ERROR] {symbol} ({label}): {e}")

        return alerts
