from decimal import Decimal

class RiskManager:
    def __init__(self, client, equity_ratio):
        self.client = client
        self.equity_ratio = equity_ratio  # Decimal 類型，例如 0.03 表示使用 3%

    async def get_order_qty(self, symbol):
        equity = await self.client.get_equity()
        equity = Decimal(str(equity))  # ✅ 強制轉為 Decimal，避免 float × Decimal 問題

        usdt_amount = equity * self.equity_ratio

        price = await self.get_price(symbol)
        if price == 0:
            return 0

        price = Decimal(str(price))  # ✅ 確保是 Decimal 型別
        qty = usdt_amount / price

        return float(qty)

    async def get_nominal_value(self, symbol, qty):
        price = await self.get_price(symbol)
        return price * qty

    async def get_price(self, symbol):
        try:
            data = self.client.client.ticker_price(symbol=symbol)
            return float(data["price"])
        except Exception as e:
            print(f"[ERROR] Failed to fetch price for {symbol}: {e}")
            return 0
