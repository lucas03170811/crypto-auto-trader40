from decimal import Decimal

class RiskManager:
    def __init__(self, client, equity_ratio):
        self.client = client
        self.equity_ratio = equity_ratio  # Decimal 類型

    async def get_order_qty(self, symbol):
        # ✅ 修正型別衝突：將 float → Decimal
        equity = Decimal(str(await self.client.get_equity()))
        usdt_amount = equity * self.equity_ratio
        price = await self.client.get_price(symbol)
        return usdt_amount / Decimal(str(price))

    async def get_nominal_value(self, symbol, qty):
        # ✅ 保留 float × float，因為下單邏輯用不到 Decimal
        price = await self.client.get_price(symbol)
        return price * qty
