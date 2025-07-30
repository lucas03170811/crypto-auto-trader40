import pandas as pd
import pandas_ta as ta
from decimal import Decimal

def revert_signal(df: pd.DataFrame):
    df.ta.bbands(length=20, append=True)
    df.ta.rsi(length=14, append=True)

    price = Decimal(df["close"].iloc[-1])
    lower = df["BBL_20_2.0"].iloc[-1]
    upper = df["BBU_20_2.0"].iloc[-1]
    rsi   = df["RSI_14"].iloc[-1]

    long  = price < Decimal(lower) and rsi < 35
    short = price > Decimal(upper) and rsi > 65

    return long, short
