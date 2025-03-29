import os
from dotenv import load_dotenv
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
)
from telegram_bot.handlers import (
    start,
    help_command,
    add_coin,
    remove_coin,
    list_watchlist,
    get_rsi,
    list_symbols,
    list_intervals,
)
from telegram_bot.alert_loop import rsi_alert_loop

# Load environment variables
load_dotenv(dotenv_path=os.path.join("private", ".env"))
TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")

if not TOKEN:
    raise RuntimeError("TELEGRAM_BOT_TOKEN not set in .env")

print("[BOT] Starting Telegram bot polling...")

# Build the app
app = ApplicationBuilder().token(TOKEN).build()

# Register command handlers
app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("help", help_command))
app.add_handler(CommandHandler("add", add_coin))
app.add_handler(CommandHandler("remove", remove_coin))
app.add_handler(CommandHandler("watchlist", list_watchlist))
app.add_handler(CommandHandler("get", get_rsi))
app.add_handler(CommandHandler("symbols", list_symbols))
app.add_handler(CommandHandler("intervals", list_intervals))

# Run background alert task AFTER app is initialized
async def post_init(application):
    application.create_task(rsi_alert_loop(application))

app.post_init = post_init

# Start the bot (manages its own asyncio loop internally)
app.run_polling()
