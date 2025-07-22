import pandas as pd
import pandas_ta as ta
from decimal import Decimal

def revert_signal(df: pd.DataFrame):
    """Return mean‑revert (long, short) booleans."""
    bb = ta.bbands(df["close"], length=20)
    rsi = ta.rsi(df["close"], length=14).iloc[-1]
    price = Decimal(df["close"].iloc[-1])

    lower, upper = bb["BBL_20_2.0"].iloc[-1], bb["BBU_20_2.0"].iloc[-1]
    long  = (price < Decimal(lower)) and (rsi < 25)
    short = (price > Decimal(upper)) and (rsi > 75)
    return long, short
