import asyncio
from strategy.trend import generate_trend_signal
from strategy.revert import generate_revert_signal
from strategy.filter import filter_symbols

class HedgeEngine:
    def __init__(self, client, risk_mgr):
        self.client = client
        self.risk_mgr = risk_mgr

    async def run(self):
        print("[Engine] Running scan...")
        symbols = await filter_symbols(self.client)
        print(f"[Engine] Filtered symbols: {symbols}")

        for symbol in symbols:
            data = await self.client.get_klines(symbol)
            if data is None:
                continue

            trend_signal = generate_trend_signal(data)
            revert_signal = generate_revert_signal(data)

            signal = trend_signal or revert_signal

            if signal:
                await self.risk_mgr.execute_trade(symbol, signal)
