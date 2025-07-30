import asyncio
from decimal import Decimal
import config

class SymbolFilter:
    def __init__(self, client):
        self.client = client

    async def fetch_metrics(self, symbol):
        try:
            premium = await self.client.futures_premium_index(symbol=symbol)
            stats = await self.client.futures_ticker(symbol=symbol)
            funding = Decimal(premium["lastFundingRate"])
            volume = Decimal(stats["quoteVolume"])
            return symbol, funding, volume
        except Exception:
            return symbol, Decimal("-1"), Decimal("0")

    async def shortlist(self):
        tasks = [self.fetch_metrics(s) for s in config.SYMBOL_POOL]
        results = await asyncio.gather(*tasks)

        selected = []
        for symbol, funding, volume in results:
            if funding >= Decimal("-0.01") and volume >= Decimal("5000000"):
                selected.append(symbol)
        return selected[:6]
