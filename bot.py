import yfinance as yf
import pandas as pd
from ta.trend import EMAIndicator

# Forex symbol, example EURUSD
symbol = "EURUSD=X"

# Historical data fetch
data = yf.download(symbol, period="1y", interval="1d")

# Close price 1D Series select
close = data['Close']

# EMA calculation
ema20 = EMAIndicator(close, 20).ema_indicator()
ema50 = EMAIndicator(close, 50).ema_indicator()

# Add EMA to DataFrame
data['EMA20'] = ema20
data['EMA50'] = ema50

# Simple crossover logic
data['Signal'] = 0
data.loc[data['EMA20'] > data['EMA50'], 'Signal'] = 1   # Buy
data.loc[data['EMA20'] < data['EMA50'], 'Signal'] = -1  # Sell

# Latest signal
latest_signal = data['Signal'].iloc[-1]
if latest_signal == 1:
    print("BUY Signal ✅")
elif latest_signal == -1:
    print("SELL Signal ❌")
else:
    print("No clear signal ⏸")

# Optional: print last 5 rows
print(data.tail())
