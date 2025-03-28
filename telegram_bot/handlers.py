from telegram import Update
from telegram.ext import ContextTypes
from telegram_bot.state import user_watchlists, save_watchlists
from rsi_monitor.monitor import INTERVALS, RSIMonitor
from rsi_monitor.utils import VALID_BASE_SYMBOLS, normalize_symbol, is_valid_symbol

ALL_SYMBOLS = [normalize_symbol(sym) for sym in VALID_BASE_SYMBOLS]


STANDARD_INTERVALS = list(INTERVALS.values())

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "👋 Welcome to the RSI Alert Bot!\n\n"
        "Commands:\n"
        "/add <symbol> <interval> – Start monitoring (e.g. /add btc 5m)\n"
        "/remove <symbol> <interval> – Stop monitoring\n"
        "/add all all – Monitor all pairs & timeframes\n"
        "/watchlist – View your current alerts\n"
        "/get <symbol> <interval> – Check current RSI\n"
        "/symbols – List supported coins\n"
        "/intervals – List available timeframes\n"
        "/help – Show full command guide"
    )


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "📖 *RSI Bot Help*\n\n"
        "/add <symbol> <interval> — Start monitoring (e.g. /add btc 5m)\n"
        "/remove <symbol> <interval> — Stop monitoring\n"
        "/add all all — Monitor all pairs & timeframes\n"
        "/watchlist — Show all your active alerts\n"
        "/get <symbol> <interval> — Get current RSI\n"
        "/symbols — List supported coins\n"
        "/intervals — List available timeframes\n"
        "/help — Show this message",
        parse_mode="Markdown"
    )


async def add_coin(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    args = context.args

    if len(args) != 2:
        return await update.message.reply_text("Usage: /add <symbol|all> <interval|all>")

    symbol_arg, interval_arg = args[0].lower(), args[1].lower()
    symbols = ALL_SYMBOLS if symbol_arg == "all" else [normalize_symbol(symbol_arg)]
    intervals = STANDARD_INTERVALS if interval_arg == "all" else [interval_arg]

    # Validate intervals
    invalid_intervals = [i for i in intervals if i not in STANDARD_INTERVALS]
    if invalid_intervals:
        return await update.message.reply_text(f"⚠️ Invalid intervals: {', '.join(invalid_intervals)}")

    # Validate symbols
    invalid_symbols = [s for s in symbols if not is_valid_symbol(s)]
    if invalid_symbols:
        return await update.message.reply_text(f"❌ Unknown symbols: {', '.join(invalid_symbols)}")

    # Add to watchlist
    user_watchlists.setdefault(user_id, set())
    new_alerts = 0

    for symbol in symbols:
        for interval in intervals:
            pair = (symbol, interval)
            if pair not in user_watchlists[user_id]:
                user_watchlists[user_id].add(pair)
                new_alerts += 1

    save_watchlists()
    await update.message.reply_text(f"✅ Added {new_alerts} new alerts.")

async def remove_coin(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    args = context.args

    if len(args) != 2:
        return await update.message.reply_text("Usage: /remove <symbol|all> <interval|all>")

    symbol_arg, interval_arg = args[0].lower(), args[1].lower()
    symbols = ALL_SYMBOLS if symbol_arg == "all" else [normalize_symbol(symbol_arg)]
    intervals = STANDARD_INTERVALS if interval_arg == "all" else [interval_arg]

    # Validate intervals
    invalid_intervals = [i for i in intervals if i not in STANDARD_INTERVALS]
    if invalid_intervals:
        return await update.message.reply_text(f"⚠️ Invalid intervals: {', '.join(invalid_intervals)}")

    # Validate symbols
    invalid_symbols = [s for s in symbols if not is_valid_symbol(s)]
    if invalid_symbols:
        return await update.message.reply_text(f"❌ Unknown symbols: {', '.join(invalid_symbols)}")

    current = user_watchlists.get(user_id, set())
    to_remove = {(s, i) for s in symbols for i in intervals}

    removed = current & to_remove
    if removed:
        user_watchlists[user_id] -= removed
        save_watchlists()
        lines = [f"- {s} ({i})" for s, i in sorted(removed)]
        return await update.message.reply_text(f"🗑 Removed:\n" + "\n".join(lines))
    else:
        return await update.message.reply_text("⚠️ None of those alerts were in your watchlist.")

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

    symbol_input, interval = args[0], args[1].lower()
    symbol = normalize_symbol(symbol_input)

    if not is_valid_symbol(symbol):
        return await update.message.reply_text(f"❌ Unknown symbol: {symbol_input.upper()}")

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
    lines = [f"- {sym}" for sym in sorted(VALID_BASE_SYMBOLS)]
    await update.message.reply_text("📜 Available symbols:\n" + "\n".join(lines))

async def list_intervals(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "⏱ Available intervals:\n" + "\n".join(f"- {i}" for i in STANDARD_INTERVALS)
    )
