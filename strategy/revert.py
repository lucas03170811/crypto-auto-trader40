import pandas as pd
import pandas_ta as ta
from decimal import Decimal

def revert_signal(df: pd.DataFrame):
    """Return mean-revert (long, short) booleans."""
    df.ta.bbands(length=20, append=True)
    df.ta.rsi(length=14, append=True)

    price = Decimal(df["close"].iloc[-1])
    lower = Decimal(df["BBL_20_2.0"].iloc[-1])
    upper = Decimal(df["BBU_20_2.0"].iloc[-1])
    rsi = Decimal(df["RSI_14"].iloc[-1])

    long  = (price < lower) and (rsi < 35)  # 放寬 RSI 條件
    short = (price > upper) and (rsi > 65)
    return long, short
