from telegram import Update
from telegram.ext import ContextTypes
from telegram_bot.state import (
    get_watchlists, add_to_watchlist, remove_from_watchlist
)
from rsi_monitor.config import INTERVALS, normalize_symbol, is_valid_symbol
from rsi_monitor.monitor import RSIMonitor

STANDARD_INTERVALS = list(INTERVALS.values())


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "👋 Welcome to the RSI Alert Bot!\n\n"
        "Commands:\n"
        "/add <symbol> <interval> – Add RSI monitoring (e.g. /add btc 5m)\n"
        "/remove <symbol> <interval> – Remove a pair\n"
        "/watchlist – View your current alerts\n"
        "/get <symbol> <interval> – Check current RSI\n"
        "/symbols – List supported coins\n"
        "/intervals – List available timeframes\n"
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
        "/symbols — List all supported coins\n"
        "/intervals — List all available timeframes\n"
        "/help — Show this message",
        parse_mode="Markdown"
    )


async def add_coin(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    args = context.args

    if len(args) != 2:
        return await update.message.reply_text("Usage: /add <symbol> <interval>")

    symbol_input, interval = args[0].lower(), args[1].lower()
    user_watchlists = get_watchlists()

    added = []

    def try_add(sym, intv):
        pair = (normalize_symbol(sym), intv)
        if pair not in user_watchlists.get(user_id, set()):
            add_to_watchlist(user_id, pair)
            added.append(pair)

    if symbol_input == "all" and interval == "all":
        for sym in ["BTC", "ETH", "BNB", "SOL", "XRP", "DOGE", "ADA", "DOT", "SUI"]:
            for intv in STANDARD_INTERVALS:
                try_add(sym, intv)

    elif symbol_input == "all":
        if interval not in STANDARD_INTERVALS:
            return await update.message.reply_text("⚠️ Invalid interval.")
        for sym in ["BTC", "ETH", "BNB", "SOL", "XRP", "DOGE", "ADA", "DOT", "SUI"]:
            try_add(sym, interval)

    elif interval == "all":
        for intv in STANDARD_INTERVALS:
            try_add(symbol_input, intv)

    else:
        if interval not in STANDARD_INTERVALS:
            return await update.message.reply_text("⚠️ Invalid interval.")
        try_add(symbol_input, interval)

    await update.message.reply_text(f"✅ Added {len(added)} new alerts.")


async def remove_coin(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    args = context.args

    if len(args) != 2:
        return await update.message.reply_text("Usage: /remove <symbol> <interval>")

    symbol_input, interval = args[0].lower(), args[1].lower()
    symbol = normalize_symbol(symbol_input)
    current = get_watchlists().get(user_id, set())

    removed = []

    if symbol_input == "all" and interval == "all":
        removed = list(current)
    elif symbol_input == "all":
        removed = [pair for pair in current if pair[1] == interval]
    elif interval == "all":
        removed = [pair for pair in current if pair[0] == symbol]
    else:
        pair = (symbol, interval)
        if pair in current:
            removed = [pair]

    for pair in removed:
        remove_from_watchlist(user_id, pair)

    if removed:
        await update.message.reply_text(f"🗑 Removed {len(removed)} alert(s).")
    else:
        await update.message.reply_text("Nothing to remove.")


async def list_watchlist(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    items = get_watchlists().get(user_id, set())
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


async def list_symbols(update: Update, context: ContextTypes.DEFAULT_TYPE):
    coins = ["BTC", "ETH", "BNB", "SOL", "XRP", "DOGE", "ADA", "DOT", "SUI"]
    await update.message.reply_text("📊 Available symbols:\n" + "\n".join(f"- {c}" for c in coins))


async def list_intervals(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("⏱ Available intervals:\n" + "\n".join(f"- {i}" for i in STANDARD_INTERVALS))
