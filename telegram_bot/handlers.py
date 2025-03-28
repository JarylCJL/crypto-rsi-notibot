from telegram import Update
from telegram.ext import ContextTypes
from telegram_bot.state import user_watchlists, save_watchlists
from rsi_monitor.monitor import INTERVALS, RSIMonitor

STANDARD_INTERVALS = list(INTERVALS.values())

def normalize_symbol(symbol: str) -> str:
    return symbol.upper().replace("USD", "USDT")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "👋 Welcome to the RSI Alert Bot!\n\n"
        "Commands:\n"
        "/add <symbol> <interval> – Add RSI monitoring (e.g. /add btc 5m)\n"
        "/remove <symbol> <interval> – Remove a pair\n"
        "/watchlist – View your current alerts\n"
        "/get <symbol> <interval> – Check current RSI\n"
        "/help – Show all available commands"
    )

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "📖 *RSI Bot Help*\n\n"
        "/add <symbol> <interval> — Start monitoring (e.g. /add btc 5m)\n"
        "/remove <symbol> <interval> — Stop monitoring\n"
        "/add all <interval> — Add available coins\n"
        "/remove <symbol> all — Remove all intervals for symbol\n"
        "/watchlist — Show all your active alerts\n"
        "/get <symbol> <interval> — Get current RSI\n"
        "/help — Show this message",
        parse_mode="Markdown"
    )

async def add_coin(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    args = context.args

    if len(args) != 2:
        return await update.message.reply_text("Usage: /add <symbol> <interval>")

    symbol_input, interval = args[0].lower(), args[1].lower()

    if interval == "all":
        return await update.message.reply_text(
            "⏱ Available intervals:\n" + "\n".join(f"- {i}" for i in STANDARD_INTERVALS)
        )

    if interval not in STANDARD_INTERVALS:
        return await update.message.reply_text(f"⚠️ Invalid interval. Valid options: {', '.join(STANDARD_INTERVALS)}")

    if symbol_input == "all":
        return await update.message.reply_text("📊 Available symbols: BTC, ETH, BNB, etc. Try /add <symbol> <interval>")

    symbol = normalize_symbol(symbol_input)

    user_watchlists.setdefault(user_id, set()).add((symbol, interval))
    save_watchlists()
    await update.message.reply_text(f"✅ Added {symbol} {interval} to your alerts.")

async def remove_coin(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    args = context.args

    if len(args) != 2:
        return await update.message.reply_text("Usage: /remove <symbol> <interval>")

    symbol_input, interval = args[0].lower(), args[1].lower()
    symbol = normalize_symbol(symbol_input)

    current = user_watchlists.get(user_id, set())

    if symbol_input == "all":
        return await update.message.reply_text("📊 Your current symbols:\n" + "\n".join({s for s, _ in current}))

    if interval == "all":
        removed = {pair for pair in current if pair[0] == symbol}
        if removed:
            user_watchlists[user_id] -= removed
            save_watchlists()
            return await update.message.reply_text(f"🗑 Removed all intervals for {symbol}")
        else:
            return await update.message.reply_text("Nothing to remove.")
    
    pair = (symbol, interval)
    if pair not in current:
        return await update.message.reply_text("❌ That pair is not in your watchlist.")
    
    user_watchlists[user_id].remove(pair)
    save_watchlists()
    await update.message.reply_text(f"🗑 Removed {symbol} {interval} from your watchlist.")

async def list_watchlist(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    items = user_watchlists.get(user_id, set())
    if not items:
        await update.message.reply_text("📭 Your watchlist is empty.")
    else:
        lines = [f"- {sym} ({intv})" for sym, intv in sorted(items)]
        await update.message.reply_text("📈 Your current alerts:\n" + "\n".join(lines))

async def get_rsi(update: Update, context: ContextTypes.DEFAULT_TYPE):
    args = context.args
    if len(args) != 2:
        return await update.message.reply_text("Usage: /get <symbol> <interval>")

    symbol = normalize_symbol(args[0])
    interval = args[1].lower()

    if interval not in STANDARD_INTERVALS:
        return await update.message.reply_text("⚠️ Invalid interval.")

    try:
        monitor = RSIMonitor([symbol])
        klines = monitor.fetch_klines(symbol, interval)
        rsi_values = monitor.compute_rsi(klines)
        current_rsi = rsi_values[-1] if rsi_values else None

        if current_rsi is not None:
            await update.message.reply_text(f"📊 RSI for {symbol} ({interval}): {current_rsi:.2f}")
        else:
            await update.message.reply_text("⚠️ Could not compute RSI.")
    except Exception as e:
        await update.message.reply_text(f"⚠️ Error: {e}")
