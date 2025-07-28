import pandas as pd
import pandas_ta as ta
from decimal import Decimal

def revert_signal(df: pd.DataFrame):
    """Return mean-revert (long, short) booleans."""
    df.ta.bbands(length=20, append=True)
    df.ta.rsi(length=14, append=True)

    price = Decimal(df["close"].iloc[-1])
    lower = df["BBL_20_2.0"].iloc[-1]
    upper = df["BBU_20_2.0"].iloc[-1]
    rsi = df["RSI_14"].iloc[-1]

    # ✅ 放寬進場條件：更靠近布林通道外緣即可，RSI 進一步放寬
    long  = (price < Decimal(lower * 1.01)) and (rsi < 35)
    short = (price > Decimal(upper * 0.99)) and (rsi > 65)
    return long, short
