import asyncio
import os
from dotenv import load_dotenv
from telegram.ext import ApplicationBuilder, CommandHandler

from telegram_bot.handlers import start, add_coin, remove_coin, list_watchlist, get_rsi, help_command, list_symbols, list_intervals
from telegram_bot.alert_loop import rsi_alert_loop
from telegram_bot.state import load_watchlists

load_dotenv(dotenv_path="./private/.env")
BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
# print("Loaded TOKEN:", BOT_TOKEN)

if not BOT_TOKEN:
    raise RuntimeError("TELEGRAM_BOT_TOKEN not set in .env")

async def bootstrap():
    load_watchlists()

    app = ApplicationBuilder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("add", add_coin))
    app.add_handler(CommandHandler("remove", remove_coin))
    app.add_handler(CommandHandler("watchlist", list_watchlist))
    app.add_handler(CommandHandler("get", get_rsi))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(CommandHandler("symbols", list_symbols))
    app.add_handler(CommandHandler("intervals", list_intervals))

    asyncio.create_task(rsi_alert_loop(app))
    await app.initialize()
    await app.start()
    await app.updater.start_polling()

# 🔒 The final magic: don't let PTB close the loop
if __name__ == "__main__":
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)

    try:
        loop.create_task(bootstrap())
        loop.run_forever()
    except KeyboardInterrupt:
        print("Bot stopped manually.")
