import numpy as np
import pandas as pd

def calculate_rsi(prices, period: int = 14):
    """
    Calculates RSI using Wilder's smoothing method (commonly used by Kraken, TradingView, etc.)
    """
    delta = np.diff(prices)
    gain = np.where(delta > 0, delta, 0)
    loss = np.where(delta < 0, -delta, 0)

    gain_series = pd.Series(gain)
    loss_series = pd.Series(loss)

    avg_gain = gain_series.ewm(alpha=1/period, min_periods=period, adjust=False).mean()
    avg_loss = loss_series.ewm(alpha=1/period, min_periods=period, adjust=False).mean()

    rs = avg_gain / avg_loss
    rsi = 100 - (100 / (1 + rs))

    return rsi.tolist()
