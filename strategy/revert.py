import pandas as pd
import pandas_ta as ta

def generate_revert_signal(data):
    df = pd.DataFrame(data, columns=['timestamp', 'open', 'high', 'low', 'close', 'volume', 'x','x','x','x','x'])
    df['close'] = pd.to_numeric(df['close'])
    df.ta.rsi(length=14, append=True)

    if df['RSI_14'].iloc[-1] < 30:
        return 'LONG'
    elif df['RSI_14'].iloc[-1] > 70:
        return 'SHORT'
    return None
