from strategy.trend import generate_trend_signal
from strategy.revert import generate_revert_signal

async def generate_signal(symbol, client):
    """
    綜合分析策略，依據趨勢優先，再考慮反轉訊號。
    """
    data = await client.get_klines(symbol)

    if not data or len(data) < 30:
        return None

    trend_signal = generate_trend_signal(data)
    revert_signal = generate_revert_signal(data)

    if trend_signal:
        print(f"[SIGNAL] {symbol} trend -> {trend_signal}")
        return trend_signal

    if revert_signal:
        print(f"[SIGNAL] {symbol} revert -> {revert_signal}")
        return revert_signal

    return None
