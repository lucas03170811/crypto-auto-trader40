import asyncio
from decimal import Decimal
from typing import List

from config import SYMBOL_POOL
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
        """Return up to 6 symbols that pass both filters."""
        tasks = [self.fetch_metrics(s) for s in SYMBOL_POOL]
        results = await asyncio.gather(*tasks, return_exceptions=True)

        approved = []
        for sym, res in zip(SYMBOL_POOL, results):
            if isinstance(res, Exception):
                continue
            funding, volume = res

            # ✅ 放寬條件：資金費率略為負值、成交量降低至 500 萬
            if funding >= Decimal("-0.003") and volume >= Decimal("5000000"):
                approved.append(sym)

        return approved[:6]
