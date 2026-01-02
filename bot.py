import yfinance as yf
import pandas as pd
import requests

TOKEN = "8523307430:AAFFDRMDmIgUIEBTUi2dRwX0JI09irLClP8"
CHAT_ID = "7768160549"
SYMBOL = "EURUSD=X"

def send_alert(message):
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage?chat_id={CHAT_ID}&text={message}"
    requests.get(url)

def check_market():
    # ડેટા મેળવવો
    df = yf.download(tickers=SYMBOL, period='5d', interval='15m', progress=False)
    
    if df.empty or len(df) < 50:
        print("Data not found!")
        return

    # EMA ગણતરી
    df['EMA20'] = df['Close'].ewm(span=20, adjust=False).mean()
    df['EMA50'] = df['Close'].ewm(span=50, adjust=False).mean()
    
    # છેલ્લી બે કેન્ડલ
    last_20 = df['EMA20'].iloc[-1]
    last_50 = df['EMA50'].iloc[-1]
    prev_20 = df['EMA20'].iloc[-2]
    prev_50 = df['EMA50'].iloc[-2]

    if prev_20 < prev_50 and last_20 > last_50:
        send_alert(f"🚀 BUY SIGNAL: {SYMBOL}")
    elif prev_20 > prev_50 and last_20 < last_50:
        send_alert(f"📉 SELL SIGNAL: {SYMBOL}")
    else:
        print("No Signal.")

if __name__ == "__main__":
    check_market()
