import asyncio
from binance import AsyncClient, BinanceSocketManager
from decimal import Decimal
from typing import Dict, List
from config import BINANCE_API_KEY, BINANCE_API_SECRET, TESTNET, MAX_LEVERAGE

class BinanceClient:
    """Light wrapper around python‑binance AsyncClient with hedge‑mode helpers."""

    def __init__(self):
        self.client: AsyncClient | None = None
        self._tickers: Dict[str, Dict] = {}

    # ---------- Init ----------
    async def initialize(self):
        self.client = await AsyncClient.create(
            BINANCE_API_KEY, BINANCE_API_SECRET,
            testnet=TESTNET,
        )
        # enable hedge mode once per account
        await self.client.futures_position_mode_change(dualSidePosition=True)
        print("[INFO] Hedge mode enabled")

    # ---------- REST helpers ----------
    async def set_leverage(self, symbol: str, leverage: int = MAX_LEVERAGE):
        try:
            await self.client.futures_change_leverage(symbol=symbol, leverage=leverage)
        except Exception as e:
            print("[WARN] set_leverage", e)

    async def place_order(self, symbol: str, side: str, positionSide: str,
                          quantity: Decimal, reduce_only: bool = False):
        params = {
            "symbol": symbol,
            "side": side,
            "type": "MARKET",
            "quantity": float(quantity),
            "positionSide": positionSide,
            "newOrderRespType": "ACK",
            "reduceOnly": reduce_only,
        }
        return await self.client.futures_create_order(**params)

    async def get_account_balance(self) -> Decimal:
        info = await self.client.futures_account_balance()
        usdt = next(b for b in info if b["asset"] == "USDT")
        return Decimal(usdt["balance"])

    # ---------- WS stream ----------
    async def price_stream(self, symbols: List[str]):
        """Yield kline messages (1 m) for the provided symbols."""
        bm = BinanceSocketManager(self.client)
        streams = [f"{s.lower()}@kline_1m" for s in symbols]
        async with bm.futures_multiplex_socket(streams) as stream:
            while True:
                msg = await stream.recv()
                if msg:
                    yield msg
