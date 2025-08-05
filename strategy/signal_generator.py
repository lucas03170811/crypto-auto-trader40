from strategy.filter import filter_symbols
from strategy.trend import generate_trend_signal
from strategy.revert import generate_revert_signal

class SignalGenerator:
    def __init__(self, client):
        self.client = client

    async def get_filtered_symbols(self, symbols):
        return await filter_symbols(self.client)

    async def generate_signal(self, symbol):
        data = await self.client.get_klines(symbol)
        if not data or len(data) < 30:
            return None

        trend_signal = generate_trend_signal(data)
        revert_signal = generate_revert_signal(data)

        # 若兩個策略方向一致，就採用該方向進場
        if trend_signal == revert_signal:
            print(f"[SIGNAL] {symbol} → {trend_signal.upper()} ✅")
            return trend_signal

        print(f"[NO MATCH] {symbol} → trend={trend_signal}, revert={revert_signal}")
        return None
