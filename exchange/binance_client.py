import asyncio
import traceback
from binance.um_futures import UMFutures

class BinanceClient:
    def __init__(self, api_key, api_secret):
        self.client = UMFutures(key=api_key, secret=api_secret)

    async def get_price(self, symbol):
        try:
            ticker = self.client.ticker_price(symbol=symbol)
            return float(ticker['price'])
        except Exception as e:
            print(f"[ERROR] Failed to get price for {symbol}: {e}")
            traceback.print_exc()
            return None

    async def get_klines(self, symbol, interval="1h", limit=50):
        try:
            klines = self.client.klines(symbol=symbol, interval=interval, limit=limit)
            return klines
        except Exception as e:
            print(f"[ERROR] Failed to get klines for {symbol}: {e}")
            traceback.print_exc()
            return []

    async def get_equity(self):
        try:
            balance = self.client.balance()
            for asset in balance:
                if asset['asset'] == 'USDT':
                    return float(asset['balance'])
        except Exception as e:
            print(f"[ERROR] Failed to get equity: {e}")
            traceback.print_exc()
        return 0

    async def get_position(self, symbol):
        try:
            positions = self.client.position_information(symbol=symbol)
            for p in positions:
                if p['positionSide'] == 'LONG':
                    return float(p['positionAmt'])
        except Exception as e:
            print(f"[ERROR] Failed to get position for {symbol}: {e}")
            traceback.print_exc()
        return 0

    async def open_long(self, symbol, qty):
        try:
            order = self.client.new_order(
                symbol=symbol,
                side="BUY",
                type="MARKET",
                quantity=qty,
                positionSide="LONG"  # ✅ 指定對沖模式方向
            )
            print(f"[ORDER] LONG {symbol} qty={qty}")
            return order
        except Exception as e:
            print(f"[OPEN LONG ERROR] {symbol}: {e}")
            if hasattr(e, 'response') and hasattr(e.response, 'text'):
                print(f"[ERROR DETAIL] {e.response.text}")
            traceback.print_exc()
            return None

    async def open_short(self, symbol, qty):
        try:
            order = self.client.new_order(
                symbol=symbol,
                side="SELL",
                type="MARKET",
                quantity=qty,
                positionSide="SHORT"  # ✅ 指定對沖模式方向
            )
            print(f"[ORDER] SHORT {symbol} qty={qty}")
            return order
        except Exception as e:
            print(f"[OPEN SHORT ERROR] {symbol}: {e}")
            if hasattr(e, 'response') and hasattr(e.response, 'text'):
                print(f"[ERROR DETAIL] {e.response.text}")
            traceback.print_exc()
            return None
