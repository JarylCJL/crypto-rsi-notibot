import asyncio
from telegram_bot.state import user_watchlists
from rsi_monitor.monitor import RSIMonitor

async def rsi_alert_loop(app):
    sent_alerts = {}

    while True:
        user_symbols = {}

        # Reorganize watchlist per user
        for user_id, pairs in user_watchlists.items():
            user_symbols[user_id] = set(pair[0] for pair in pairs)

        for user_id, symbols in user_symbols.items():
            monitor = RSIMonitor(list(symbols))
            try:
                alerts = monitor.poll()
                for symbol, interval, rsi, threshold, direction in alerts:
                    if (symbol, interval) not in user_watchlists[user_id]:
                        continue

                    key = (user_id, symbol, interval, threshold, direction)
                    if sent_alerts.get(key):
                        continue

                    msg = (
                        f"🚨 *RSI Alert!*\n\n"
                        f"Symbol: `{symbol}`\n"
                        f"Interval: `{interval}`\n"
                        f"RSI: *{rsi:.2f}* crossed *{direction.upper()}* {threshold}"
                    )
                    await app.bot.send_message(chat_id=user_id, text=msg, parse_mode="Markdown")
                    sent_alerts[key] = True
            except Exception as e:
                print(f"[Polling Error] {e}")
        await asyncio.sleep(60)
