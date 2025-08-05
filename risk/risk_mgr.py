from config import BASE_QTY

class RiskManager:
    def __init__(self, client):
        self.client = client

    async def execute_trade(self, symbol, signal):
        signal = signal.lower()
        position = await self.client.get_position(symbol)
        print(f"[Position] {symbol}: {position}")  # 🔍 新增 log

        try:
            if signal == 'long' and position <= 0:
                print(f"[Trade] Entering LONG {symbol}")
                await self.client.open_long(symbol, BASE_QTY)

            elif signal == 'short' and position >= 0:
                print(f"[Trade] Entering SHORT {symbol}")
                await self.client.open_short(symbol, BASE_QTY)
        except Exception as e:
            print(f"[TRADE ERROR] {symbol}: {e}")
