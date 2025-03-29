import json
import os

WATCHLISTS_FILE = os.path.join("private", "watchlists.json")
user_watchlists = {}  # made public again for use in alert_loop


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
    # print("[DEBUG] save_watchlists() called")
    # print("[DEBUG] Current state:", user_watchlists)


def get_watchlists():
    return user_watchlists


def add_to_watchlist(user_id, pair):
    user_watchlists.setdefault(user_id, set()).add(pair)
    save_watchlists()


def remove_from_watchlist(user_id, pair):
    if user_id in user_watchlists and pair in user_watchlists[user_id]:
        user_watchlists[user_id].remove(pair)
        if not user_watchlists[user_id]:
            del user_watchlists[user_id]
        save_watchlists()
