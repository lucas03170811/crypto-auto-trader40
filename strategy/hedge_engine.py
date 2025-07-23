from decimal import Decimal
from exchange.binance_client import BinanceClient
from config import MAX_LEVERAGE

class HedgeEngine:
    """Manage dual​-side hedge entries and exits."""

    def __init__(self, client: BinanceClient, risk_mgr):
        self.client = client
        self.risk_mgr = risk_mgr
        self.active_hedges = {}  # symbol -> {entry_price, qty}

    async def open_dual(self, symbol: str):
        price = await self._get_price(symbol)
        qty = (self.risk_mgr.base_qty * MAX_LEVERAGE) / price
        qty = qty.quantize(Decimal("0.001"))
        await self.client.place_order(symbol, "BUY",  "LONG",  qty)
        await self.client.place_order(symbol, "SELL", "SHORT", qty)
        self.active_hedges[symbol] = {
            "entry_price": price,
            "qty": qty,
        }
        print(f"[HEDGE] Opened dual {symbol} qty={qty}")

    async def close_side(self, symbol: str, side: str):
        data = self.active_hedges.get(symbol)
        if not data:
            return
        qty = data["qty"]
        if side == "LONG":
            await self.client.place_order(symbol, "SELL", "LONG", qty, reduce_only=True)
        else:
            await self.client.place_order(symbol, "BUY", "SHORT", qty, reduce_only=True)
        print(f"[HEDGE] Closed {side} of {symbol}")

    async def _get_price(self, symbol: str) -> Decimal:
        t = await self.client.client.futures_symbol_ticker(symbol=symbol)
        return Decimal(t["price"])
