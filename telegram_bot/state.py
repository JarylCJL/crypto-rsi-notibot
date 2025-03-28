import json
import os

WATCHLISTS_FILE = "watchlists.json"
user_watchlists = {}  # user_id → set of (symbol, interval)

def load_watchlists():
    global user_watchlists
    if os.path.exists(WATCHLISTS_FILE):
        with open(WATCHLISTS_FILE, "r") as f:
            raw = json.load(f)
            user_watchlists = {
                int(uid): set(tuple(pair) for pair in pairs)
                for uid, pairs in raw.items()
            }
    else:
        user_watchlists = {}

def save_watchlists():
    with open(WATCHLISTS_FILE, "w") as f:
        json.dump({uid: list(pairs) for uid, pairs in user_watchlists.items()}, f, indent=2)
