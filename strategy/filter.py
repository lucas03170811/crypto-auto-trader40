import asyncio
from decimal import Decimal
from typing import List

from config import FUNDING_RATE_MIN, VOLUME_MIN_USD, SYMBOL_POOL
from exchange.binance_client import BinanceClient

class SymbolFilter:
    def __init__(self, client: BinanceClient):
        self.client = client

    async def fetch_metrics(self, symbol: str):
        try:
            premium = await self.client.client.futures_premium_index(symbol=symbol)
            funding = Decimal(premium["lastFundingRate"])
            stats = await self.client.client.futures_ticker(symbol=symbol)
            volume = Decimal(stats["quoteVolume"])
            return symbol, funding, volume
        except Exception:
            return symbol, None, None

    async def shortlist(self) -> List[str]:
        tasks = [self.fetch_metrics(s) for s in SYMBOL_POOL]
        results = await asyncio.gather(*tasks)

        approved = []
        for symbol, funding, volume in results:
            if funding is None or volume is None:
                continue
            if funding >= FUNDING_RATE_MIN and volume >= VOLUME_MIN_USD:
                approved.append(symbol)

        return approved[:8]  # 最多選 8 檔
