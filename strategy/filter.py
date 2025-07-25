import asyncio
from decimal import Decimal
from typing import List

from config import FUNDING_RATE_MIN, VOLUME_MIN_USD, SYMBOL_POOL
from exchange.binance_client import BinanceClient

class SymbolFilter:
    """Screen symbols by funding‑rate and 24 h volume."""

    def __init__(self, client: BinanceClient):
        self.client = client

    async def fetch_metrics(self, symbol: str):
        """Return (funding_rate, 24h_quote_volume)."""
        premium = await self.client.client.futures_premium_index(symbol=symbol)
        funding = Decimal(premium["lastFundingRate"])
        stats = await self.client.client.futures_ticker(symbol=symbol)
        volume = Decimal(stats["quoteVolume"])
        return funding, volume

    async def shortlist(self) -> List[str]:
        """Return up to 4 symbols that pass both filters."""
        tasks = [self.fetch_metrics(s) for s in SYMBOL_POOL]
        results = await asyncio.gather(*tasks, return_exceptions=True)

        approved = []
        for sym, res in zip(SYMBOL_POOL, results):
            if isinstance(res, Exception):
                continue
            funding, volume = res
            if funding >= FUNDING_RATE_MIN and volume >= VOLUME_MIN_USD:
                approved.append(sym)

        return approved[:4]
