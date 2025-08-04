import pandas as pd
import pandas_ta as ta

def generate_trend_signal(data):
    df = pd.DataFrame(data, columns=[
        'timestamp', 'open', 'high', 'low', 'close', 'volume',
        'close_time', 'quote_asset_volume', 'num_trades',
        'taker_buy_base_vol', 'taker_buy_quote_vol', 'ignore'
    ])
    df['close'] = df['close'].astype(float)

    df['ema_short'] = ta.ema(df['close'], length=9)
    df['ema_long'] = ta.ema(df['close'], length=21)
    macd = ta.macd(df['close'], fast=12, slow=26, signal=9)
    df['macd'] = macd['MACD_12_26_9']
    df['macds'] = macd['MACDs_12_26_9']

    if df['ema_short'].iloc[-1] > df['ema_long'].iloc[-1] and df['macd'].iloc[-1] > df['macds'].iloc[-1]:
        return 'long'
    elif df['ema_short'].iloc[-1] < df['ema_long'].iloc[-1] and df['macd'].iloc[-1] < df['macds'].iloc[-1]:
        return 'short'
    return None
