import asyncio
from decimal import Decimal
from typing import List
import pandas as pd

from config import BASE_QTY, MAX_PYRAMID_LAYERS
from engine.trend import trend_signal
from engine.revert import revert_signal
from exchange.binance_client import BinanceClient
from strategy.filter import SymbolFilter


class HedgeEngine:
    def __init__(self, client: BinanceClient):
        self.client = client
        self.symbol_filter = SymbolFilter(client)
        self.open_positions = {}

    async def fetch_klines(self, symbol: str, interval: str = "15m", limit: int = 100) -> pd.DataFrame:
        klines = await self.client.client.futures_klines(symbol=symbol, interval=interval, limit=limit)
        df = pd.DataFrame(klines, columns=[
            "timestamp", "open", "high", "low", "close", "volume",
            "close_time", "quote_volume", "num_trades",
            "taker_buy_base_volume", "taker_buy_quote_volume", "ignore"
        ])
        df = df.astype({"open": float, "high": float, "low": float, "close": float, "volume": float})
        return df

    async def evaluate_symbol(self, symbol: str):
        df = await self.fetch_klines(symbol)
        long, short, adx = trend_signal(df)
        rv_long, rv_short = revert_signal(df)

        print(f"[DEBUG] {symbol} - Trend: long={long}, short={short}, ADX={adx:.2f} | Revert: long={rv_long}, short={rv_short}")

        if long or rv_long:
            await self.place_order(symbol, side="BUY")
        elif short or rv_short:
            await self.place_order(symbol, side="SELL")

    async def place_order(self, symbol: str, side: str):
        position = self.open_positions.get(symbol, {"layers": 0})

        if position["layers"] >= MAX_PYRAMID_LAYERS:
            print(f"[INFO] Max pyramid layers reached for {symbol}. Skipping...")
            return

        qty = await self.client.calculate_order_quantity(symbol, BASE_QTY)
        order = await self.client.open_position(symbol, qty, side)

        if order:
            position["layers"] += 1
            self.open_positions[symbol] = position
            print(f"[TRADE] {symbol} {side} @ {order['avgPrice']} (Layer {position['layers']})")

    async def run(self):
        while True:
            try:
                print("[INFO] Fetching shortlist...")
                shortlist = await self.symbol_filter.shortlist()

                if not shortlist:
                    print("\u274c 沒有符合條件的幣種，等待 60 秒重試...")
                    await asyncio.sleep(60)
                    continue

                tasks = [self.evaluate_symbol(symbol) for symbol in shortlist]
                await asyncio.gather(*tasks)

                print("[INFO] 任務完成，等待 60 秒...")
                await asyncio.sleep(60)
            except Exception as e:
                print(f"[ERROR] {e}")
                await asyncio.sleep(60)

