import numpy as np
import pandas as pd


def atr(df, period=14):
high, low, close = df["High"], df["Low"], df["Close"]
prev_close = close.shift(1)
tr = pd.concat([high - low, (high - prev_close).abs(), (low - prev_close).abs()], axis=1).max(axis=1)
return tr.rolling(period).mean()


def zigzag_atr(df, atr_mult=5.0, atr_period=14):
"""
ATR‑multiplier ZigZag on Close.
A new pivot prints when price moves atr_mult * ATR from the last pivot price.
"""
zz = []
atr_vals = atr(df, atr_period)
closes = df["Close"].values
idx = df.index
if len(df) < atr_period + 5:
return pd.DataFrame(columns=["index","price","type"])


last_pivot_idx = atr_period
last_pivot_price = closes[last_pivot_idx]
last_type = 0 # 1 = high, -1 = low, 0 = init
zz.append((idx[last_pivot_idx], last_pivot_price, 0))


for i in range(atr_period+1, len(df)):
threshold = atr_mult * atr_vals.iloc[i] if np.isfinite(atr_vals.iloc[i]) else np.nan
if not np.isfinite(threshold):
continue
move = closes[i] - last_pivot_price
if move >= threshold and last_type != 1:
last_pivot_idx = i; last_pivot_price = closes[i]; last_type = 1
zz.append((idx[i], closes[i], 1))
elif -move >= threshold and last_type != -1:
last_pivot_idx = i; last_pivot_price = closes[i]; last_type = -1
zz.append((idx[i], closes[i], -1))


return pd.DataFrame(zz, columns=["index","price","type"]).reset_index(drop=True)
