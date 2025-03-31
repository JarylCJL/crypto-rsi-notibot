import time
from rsi_monitor.monitor import RSIMonitor

# Define the symbols you want to monitor
WATCHLIST = ['BTCUSDT', 'ETHUSDT', 'SOLUSDT', 'ADAUSDT', 'XRPUSDT', 'SUIUSDT']

def main():
    monitor = RSIMonitor(WATCHLIST)
    
    while True:
        print(f"\n--- Polling @ {time.strftime('%Y-%m-%d %H:%M:%S')} ---")
        try:
            alerts = monitor.poll()
            for symbol, interval, rsi, threshold, direction in alerts:
                print(f"[ALERT] {symbol} ({interval}) RSI={rsi:.2f} crossed {direction} {threshold}")
        except Exception as e:
            print(f"[ERROR] {e}")
        
        time.sleep(10)

if __name__ == "__main__":
    main()
