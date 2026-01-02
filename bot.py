import yfinance as yf
import pandas as pd
import requests

# તમારી વિગતો
TOKEN = "8523307430:AAFFDRMDmIgUIEBTUi2dRwX0JI09irLClP8"
CHAT_ID = "7768160549"
SYMBOL = "EURUSD=X"

def send_alert(message):
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage?chat_id={CHAT_ID}&text={message}"
    requests.get(url)

def check_market():
    # 5 દિવસનો ડેટા
    data = yf.download(tickers=SYMBOL, period='5d', interval='15m', progress=False)
    
    if data.empty:
        return

    # EMA ગણતરી
    data['EMA20'] = data['Close'].ewm(span=20, adjust=False).mean()
    data['EMA50'] = data['Close'].ewm(span=50, adjust=False).mean()
    
    c_20, c_50 = data['EMA20'].iloc[-1], data['EMA50'].iloc[-1]
    p_20, p_50 = data['EMA20'].iloc[-2], data['EMA50'].iloc[-2]

    # ક્રોસઓવર લોજિક
    if p_20 < p_50 and c_20 > c_50:
        send_alert(f"🚀 BUY: {SYMBOL} (15m) - Green crossed above Red")
    elif p_20 > p_50 and c_20 < c_50:
        send_alert(f"📉 SELL: {SYMBOL} (15m) - Green crossed below Red")
    else:
        print("કોઈ ક્રોસઓવર નથી.")

if __name__ == "__main__":
    check_market()
