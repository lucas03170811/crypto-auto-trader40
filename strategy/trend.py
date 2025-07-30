import pandas as pd
import pandas_ta as ta

def generate_trend_signal(data):
    df = pd.DataFrame(data, columns=['timestamp', 'open', 'high', 'low', 'close', 'volume', 'x','x','x','x','x'])
    df['close'] = pd.to_numeric(df['close'])
    df.ta.ema(length=20, append=True)
    df.ta.ema(length=50, append=True)

    if df['EMA_20'].iloc[-1] > df['EMA_50'].iloc[-1]:
        return 'LONG'
    elif df['EMA_20'].iloc[-1] < df['EMA_50'].iloc[-1]:
        return 'SHORT'
    return None
