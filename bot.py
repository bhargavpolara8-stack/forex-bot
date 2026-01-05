# bot.py

import yfinance as yf
import pandas as pd
from ta.trend import EMAIndicator
import requests
import time

# -----------------------------
# Telegram setup
# -----------------------------
TELEGRAM_BOT_TOKEN = "YOUR_BOT_TOKEN"   # Replace with your bot token
TELEGRAM_CHAT_ID = "YOUR_CHAT_ID"       # Replace with your chat id

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
TICKER = "EURUSD=X"   # Change to your preferred Forex pair
INTERVAL = "1h"       # 1-hour data, can use "1d", "15m", etc.
PERIOD = "60d"        # last 60 days

# -----------------------------
# EMA crossover check
# -----------------------------
def check_ema_crossover():
    # Fetch data
    df = yf.download(TICKER, period=PERIOD, interval=INTERVAL)
    
    if df.empty:
        print("No data received from yfinance.")
        return
    
    # Fix: take 'Close' column as 1D Series
    close = df['Close']  

    # Calculate EMA
    ema20 = EMAIndicator(close, 20).ema_indicator()
    ema50 = EMAIndicator(close, 50).ema_indicator()

    # Previous candle EMA
    prev_ema20 = ema20.iloc[-2]
    prev_ema50 = ema50.iloc[-2]
    
    # Current candle EMA
    curr_ema20 = ema20.iloc[-1]
    curr_ema50 = ema50.iloc[-1]

    # Check crossover
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
