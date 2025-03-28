# 📈 Crypto RSI NotiBot

A Telegram bot that monitors the RSI (Relative Strength Index) of crypto pairs in real-time and notifies users when thresholds are crossed. Built for traders who want to catch momentum swings without staring at charts.

---

## 🚀 Features

- ✅ Monitors RSI for 5m, 15m, and 1h intervals
- ✅ Threshold alerts (crosses 70/30, 75/25, 80/20)
- ✅ Avoids spam with reset-before-realert logic
- ✅ Supports Binance and Kraken APIs
- ✅ Users can manage their own watchlists
- ✅ Fully multi-user and privacy-aware
- ✅ Persistent storage for alerts (optional)

---

## 🛠 Commands

### Core
- `/start` — Welcome message & intro
- `/help` — Full command overview

### Watchlist Management
- `/add <symbol> <interval>` — Add monitoring (e.g. `/add btc 5m`)
- `/add btc all` — Add all intervals for BTC
- `/add all 5m` — Add 5m alerts for all supported coins
- `/add all all` — Add all coins and all timeframes

- `/remove <symbol> <interval>` — Remove a pair
- `/remove btc all` — Remove all intervals for BTC
- `/remove all 5m` — Remove 5m interval from all coins
- `/remove all all` — Remove everything

- `/watchlist` — View your current alerts

### RSI Data
- `/get <symbol> <interval>` — Get current RSI for a pair

### Utility
- `/symbols` — List all supported coins
- `/intervals` — List all available timeframes

---

## 🧠 How It Works

- Bot polls exchange APIs (Binance or Kraken) every 60s
- Computes RSI-14 from OHLC data
- Checks if RSI crosses set thresholds
- Sends Telegram alerts only when thresholds are re-crossed
- Each user gets an isolated watchlist

---

## 🧑‍💻 Made by Jaryl CJL
Pull requests, issues and suggestions are welcome!

