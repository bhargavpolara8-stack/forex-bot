import os
import yfinance as yf
import requests
import time
from ta.trend import EMAIndicator

BOT_TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")

symbol = "EURUSD=X"
interval = "5m"
period = "2d"
last_signal = None

def send(msg):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    requests.post(url, data={"chat_id": CHAT_ID, "text": msg})

while True:
    data = yf.download(symbol, interval=interval, period=period)
    close = data['Close']

    ema20 = EMAIndicator(close, 20).ema_indicator()
    ema50 = EMAIndicator(close, 50).ema_indicator()

    if ema20.iloc[-2] < ema50.iloc[-2] and ema20.iloc[-1] > ema50.iloc[-1]:
        if last_signal != "BUY":
            send("📈 BUY SIGNAL\nEMA 20 crossed ABOVE EMA 50")
            last_signal = "BUY"

    if ema20.iloc[-2] > ema50.iloc[-2] and ema20.iloc[-1] < ema50.iloc[-1]:
        if last_signal != "SELL":
            send("📉 SELL SIGNAL\nEMA 20 crossed BELOW EMA 50")
            last_signal = "SELL"

    time.sleep(60)
