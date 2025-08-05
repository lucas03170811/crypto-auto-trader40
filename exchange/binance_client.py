from binance.um_futures import UMFutures
import os
import traceback

class BinanceClient:
    def __init__(self):
        self.client = None

    async def initialize(self):
        api_key = os.getenv("BINANCE_API_KEY")
        api_secret = os.getenv("BINANCE_API_SECRET")
        self.client = UMFutures(key=api_key, secret=api_secret)

    async def get_klines(self, symbol, interval='15m', limit=100):
        try:
            return self.client.klines(symbol=symbol, interval=interval, limit=limit)
        except Exception as e:
            print(f"[KLINE ERROR] {symbol}: {e}")
            return []

    async def get_current_price(self, symbol):
        try:
            ticker = self.client.ticker_price(symbol=symbol)
            return float(ticker["price"])
        except Exception as e:
            print(f"[PRICE ERROR] {symbol}: {e}")
            return 0

    async def get_position(self, symbol):
        try:
            positions = self.client.get_position_risk()
            for p in positions:
                if p["symbol"] == symbol:
                    return float(p["positionAmt"])
        except Exception as e:
            print(f"[POSITION ERROR] {symbol}: {e}")
        return 0

    async def open_long(self, symbol, qty):
        try:
            price = await self.get_current_price(symbol)
            notional = price * float(qty)

            if notional < 5:
                print(f"[SKIP ORDER] LONG {symbol} 名目價值太低: {notional:.2f} USDT（低於最低限制）")
                return None

            order = self.client.new_order(symbol=symbol, side="BUY", type="MARKET", quantity=qty)
            print(f"[ORDER] LONG {symbol} qty={qty} → 約 {notional:.2f} USDT")
            return order
        except Exception as e:
            print(f"[OPEN LONG ERROR] {symbol}: {e}")
            if hasattr(e, 'response') and hasattr(e.response, 'text'):
                print(f"[ERROR DETAIL] {e.response.text}")
            else:
                traceback.print_exc()
            return None

    async def open_short(self, symbol, qty):
        try:
            price = await self.get_current_price(symbol)
            notional = price * float(qty)

            if notional < 5:
                print(f"[SKIP ORDER] SHORT {symbol} 名目價值太低: {notional:.2f} USDT（低於最低限制）")
                return None

            order = self.client.new_order(symbol=symbol, side="SELL", type="MARKET", quantity=qty)
            print(f"[ORDER] SHORT {symbol} qty={qty} → 約 {notional:.2f} USDT")
            return order
        except Exception as e:
            print(f"[OPEN SHORT ERROR] {symbol}: {e}")
            if hasattr(e, 'response') and hasattr(e.response, 'text'):
                print(f"[ERROR DETAIL] {e.response.text}")
            else:
                traceback.print_exc()
            return None

    async def get_equity(self):
        try:
            balance = self.client.balance()
            usdt = next((b for b in balance if b["asset"] == "USDT"), {})
            return float(usdt.get("balance", 0))
        except Exception as e:
            print(f"[EQUITY ERROR] {e}")
            return 0
