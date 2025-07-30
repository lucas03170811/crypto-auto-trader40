from binance import AsyncClient

class BinanceClient:
    def __init__(self):
        self.client = None

    async def initialize(self):
        self.client = await AsyncClient.create()

    async def get_klines(self, symbol):
        try:
            data = await self.client.get_klines(symbol=symbol, interval='15m', limit=100)
            return data
        except Exception as e:
            print(f"[KLINE ERROR] {symbol}: {e}")
            return None

    async def get_position(self, symbol):
        return 0  # 模擬倉位

    async def open_long(self, symbol, qty):
        print(f"[ORDER] LONG {symbol} qty={qty}")

    async def open_short(self, symbol, qty):
        print(f"[ORDER] SHORT {symbol} qty={qty}")

    async def get_equity(self):
        return 10000
