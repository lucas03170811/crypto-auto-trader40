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
        try:
            premium = await self.client.client.futures_premium_index(symbol=symbol)
            funding = Decimal(premium["lastFundingRate"])

            stats = await self.client.client.futures_ticker(symbol=symbol)
            volume = Decimal(stats["quoteVolume"])
            return symbol, funding, volume
        except Exception as e:
            print(f"❌ 無法獲取 {symbol} 資料：{e}")
            return symbol, None, None

    async def shortlist(self) -> List[str]:
        """Return up to 6 symbols that pass both filters."""
        tasks = [self.fetch_metrics(s) for s in SYMBOL_POOL]
        results = await asyncio.gather(*tasks)

        approved = []

        for symbol, funding, volume in results:
            if funding is None or volume is None:
                continue

            if funding >= FUNDING_RATE_MIN and volume >= VOLUME_MIN_USD:
                approved.append(symbol)
            else:
                reason = []
                if funding < FUNDING_RATE_MIN:
                    reason.append(f"資金費率過低 {funding}")
                if volume < VOLUME_MIN_USD:
                    reason.append(f"成交量過小 {volume}")
                print(f"⛔ 排除 {symbol}：{'，'.join(reason)}")

        return approved[:6]  # 最多選 6 檔
