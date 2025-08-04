import pandas as pd
import pandas_ta as ta

def generate_revert_signal(data):
    df = pd.DataFrame(data, columns=[
        'timestamp', 'open', 'high', 'low', 'close', 'volume',
        'close_time', 'quote_asset_volume', 'num_trades',
        'taker_buy_base_vol', 'taker_buy_quote_vol', 'ignore'
    ])
    df['close'] = df['close'].astype(float)

    df['rsi'] = ta.rsi(df['close'], length=14)
    bb = ta.bbands(df['close'], length=20, std=2)
    df['lower_band'] = bb['BBL_20_2.0']
    df['upper_band'] = bb['BBU_20_2.0']

    latest_rsi = df['rsi'].iloc[-1]
    latest_price = df['close'].iloc[-1]
    lower_band = df['lower_band'].iloc[-1]
    upper_band = df['upper_band'].iloc[-1]

    if latest_rsi < 35 and latest_price < lower_band:
        return 'long'
    elif latest_rsi > 65 and latest_price > upper_band:
        return 'short'
    return None
