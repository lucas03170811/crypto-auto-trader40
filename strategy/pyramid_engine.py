from decimal import Decimal
from typing import Dict

from config import MAX_LEVERAGE
from exchange.binance_client import BinanceClient

class PyramidEngine:
    """Add‑on entries only in direction of profit, up to N layers."""

    def __init__(self, client: BinanceClient, risk_mgr):
        self.client = client
        self.risk_mgr = risk_mgr
        self.layers: Dict[str, int] = {}
        self.last_add_price: Dict[str, Decimal] = {}

    async def try_add(self, symbol: str, direction: str, current_price: Decimal):
        layer = self.layers.get(symbol, 0)
        if layer >= self.risk_mgr.max_layers:
            return

        # enforce min price movement (0.4 %) between add‑ons
        if symbol in self.last_add_price:
            delta = abs((current_price - self.last_add_price[symbol]) / self.last_add_price[symbol])
            if delta < Decimal("0.004"):
                return

        qty = (self.risk_mgr.base_qty * (Decimal("0.8") ** layer) * MAX_LEVERAGE) / current_price
        qty = round(float(qty), 3)
        side = "BUY" if direction == "LONG" else "SELL"

        await self.client.place_order(symbol, side, direction, qty)
        self.layers[symbol] = layer + 1
        self.last_add_price[symbol] = current_price
        print(f"[PYRAMID] {symbol} +layer {layer+1} qty={qty}")

    async def close_all(self, symbol: str, direction: str):
        side = "SELL" if direction == "LONG" else "BUY"
        pos = await self.client.client.futures_position_information(symbol=symbol)

        for p in pos:
            if p["positionSide"] == direction and Decimal(p["positionAmt"]) != 0:
                qty = abs(float(p["positionAmt"]))
                await self.client.place_order(symbol, side, direction, qty, reduce_only=True)

        self.layers.pop(symbol, None)
        self.last_add_price.pop(symbol, None)
        print(f"[EXIT] {symbol} closed all {direction}")
