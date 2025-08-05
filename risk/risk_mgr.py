from config import BASE_QTY

class RiskManager:
    def __init__(self, client):
        self.client = client

    async def execute_trade(self, symbol, signal):
        position = await self.client.get_position(symbol)

        if signal == 'LONG' and position <= 0:
            print(f"[Trade] Entering LONG {symbol}")
            await self.client.open_long(symbol, BASE_QTY)

        elif signal == 'SHORT' and position >= 0:
            print(f"[Trade] Entering SHORT {symbol}")
            await self.client.open_short(symbol, BASE_QTY)

    async def update_equity(self):
        equity = await self.client.get_equity()
        print(f"[Equity] Current equity: {equity:.2f} USDT")
