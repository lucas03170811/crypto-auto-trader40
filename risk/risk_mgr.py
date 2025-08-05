from config import BASE_QTY

class RiskManager:
    def __init__(self, client):
        self.client = client

    async def execute_trade(self, symbol, signal):
        signal = signal.lower()  # 統一大小寫
        position = await self.client.get_position(symbol)

        print(f"[Position] {symbol} current position: {position}, signal: {signal}")

        if signal == 'long':
            if position <= 0:
                print(f"[Trade] Entering LONG {symbol}")
                result = await self.client.open_long(symbol, BASE_QTY)
                if result is None:
                    print(f"[ERROR] Failed to open LONG position for {symbol}")
            else:
                print(f"[SKIP] Already holding LONG for {symbol} (position = {position})")

        elif signal == 'short':
            if position >= 0:
                print(f"[Trade] Entering SHORT {symbol}")
                result = await self.client.open_short(symbol, BASE_QTY)
                if result is None:
                    print(f"[ERROR] Failed to open SHORT position for {symbol}")
            else:
                print(f"[SKIP] Already holding SHORT for {symbol} (position = {position})")

    async def update_equity(self):
        equity = await self.client.get_equity()
        print(f"[Equity] Current equity: {equity}")
