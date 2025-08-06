from decimal import Decimal, getcontext

class RiskManager:
    def __init__(self, client, equity_ratio=0.05):
        self.client = client
        self.equity_ratio = Decimal(str(equity_ratio))  # ⬅️ 保證是 Decimal 型態
        self.min_notional = 5  # 可調整最小名目價值

    async def get_order_qty(self, symbol):
        equity = await self.client.get_equity()
        usdt_amount = Decimal(str(equity)) * self.equity_ratio  # ⬅️ 轉換 float ➜ Decimal
        price = await self.client.get_price(symbol)
        if price is None:
            return 0
        qty = usdt_amount / Decimal(str(price))
        notional = qty * Decimal(str(price))
        if notional < self.min_notional:
            print(f"[SKIP] {symbol} 名目價值 {notional:.2f} < 最小門檻 {self.min_notional}")
            return 0
        return float(qty)
