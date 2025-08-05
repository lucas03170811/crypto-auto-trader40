import asyncio
from binance.um_futures import UMFutures
import os

class BinanceClient:
    def __init__(self, api_key, api_secret):
        self.client = UMFutures(api_key=api_key, api_secret=api_secret, base_url="https://fapi.binance.com")

    async def get_klines(self, symbol, interval="15m", limit=100):
        try:
            loop = asyncio.get_event_loop()
            return await loop.run_in_executor(None, lambda: self.client.klines(symbol=symbol, interval=interval, limit=limit))
        except Exception as e:
            print(f"[ERROR] Failed to fetch klines for {symbol}: {e}")
            return None

    async def get_price(self, symbol):
        try:
            loop = asyncio.get_event_loop()
            ticker = await loop.run_in_executor(None, lambda: self.client.ticker_price(symbol=symbol))
            return float(ticker["price"])
        except Exception as e:
            print(f"[ERROR] Failed to get price for {symbol}: {e}")
            return 0.0

    async def get_equity(self):
        try:
            loop = asyncio.get_event_loop()
            info = await loop.run_in_executor(None, lambda: self.client.balance())
            for asset in info:
                if asset["asset"] == "USDT":
                    return float(asset["balance"])
        except Exception as e:
            print(f"[ERROR] Failed to get equity: {e}")
        return 0.0

    async def get_position(self, symbol):
        try:
            loop = asyncio.get_event_loop()
            result = await loop.run_in_executor(None, lambda: self.client.get_position_risk())
            for pos in result:
                if pos["symbol"] == symbol:
                    amt = float(pos["positionAmt"])
                    return amt
        except Exception as e:
            print(f"[ERROR] Failed to get position for {symbol}: {e}")
        return 0.0

    async def open_long(self, symbol, qty):
        try:
            loop = asyncio.get_event_loop()
            await loop.run_in_executor(None, lambda: self.client.new_order(
                symbol=symbol,
                side="BUY",
                type="MARKET",
                quantity=qty,
            ))
            print(f"[ORDER] LONG {symbol} qty={qty}")
        except Exception as e:
            print(f"[ERROR] Failed to open long for {symbol}: {e}")

    async def open_short(self, symbol, qty):
        try:
            loop = asyncio.get_event_loop()
            await loop.run_in_executor(None, lambda: self.client.new_order(
                symbol=symbol,
                side="SELL",
                type="MARKET",
                quantity=qty,
            ))
            print(f"[ORDER] SHORT {symbol} qty={qty}")
        except Exception as e:
            print(f"[ERROR] Failed to open short for {symbol}: {e}")
