# bot.py

import yfinance as yf
import pandas as pd
from ta.trend import EMAIndicator
import requests
import time

# -----------------------------
# Telegram setup
# -----------------------------
TELEGRAM_BOT_TOKEN = "AAHjHtoVWGyzf08_0CzoLcJfyD9t_QV10gk"
TELEGRAM_CHAT_ID = "7768160549"

def send_telegram(msg):
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    payload = {"chat_id": TELEGRAM_CHAT_ID, "text": msg}
    try:
        requests.get(url, params=payload)
    except Exception as e:
        print("Telegram send error:", e)

# -----------------------------
# Forex pair setup
# -----------------------------
TICKER = "EURUSD=X"
INTERVAL = "1h"
PERIOD = "60d"

# -----------------------------
# EMA crossover check
# -----------------------------
def check_ema_crossover():
    df = yf.download(TICKER, period=PERIOD, interval=INTERVAL)
    
    if df.empty:
        print("No data received from yfinance.")
        return
    
    # Fix: make Close 1D
    close = df['Close'].squeeze()

    ema20 = EMAIndicator(close, 20).ema_indicator()
    ema50 = EMAIndicator(close, 50).ema_indicator()

    prev_ema20 = ema20.iloc[-2]
    prev_ema50 = ema50.iloc[-2]
    
    curr_ema20 = ema20.iloc[-1]
    curr_ema50 = ema50.iloc[-1]

    if prev_ema20 < prev_ema50 and curr_ema20 > curr_ema50:
        send_telegram(f"✅ BUY signal for {TICKER} at {df.index[-1]} | Close={close.iloc[-1]:.5f}")
        print("BUY signal sent")
    elif prev_ema20 > prev_ema50 and curr_ema20 < curr_ema50:
        send_telegram(f"❌ SELL signal for {TICKER} at {df.index[-1]} | Close={close.iloc[-1]:.5f}")
        print("SELL signal sent")
    else:
        print("No signal")

# -----------------------------
# Main loop
# -----------------------------
if __name__ == "__main__":
    while True:
        try:
            check_ema_crossover()
        except Exception as e:
            print("Error:", e)
            send_telegram(f"Bot Error: {e}")
        time.sleep(60*60)  # run every 1 hour
