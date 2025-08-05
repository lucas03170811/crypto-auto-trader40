class RiskManager:
    def __init__(self, client, equity_ratio):
        self.client = client
        self.equity_ratio = equity_ratio  # 每次下單佔用的資金比重

    async def get_order_qty(self, symbol):
        # 根據帳戶資金與市價估算下單數量
        equity = await self.client.get_equity()
        usdt_amount = equity * self.equity_ratio
        price = await self.client.get_price(symbol)
        return usdt_amount / price

    async def get_nominal_value(self, symbol, qty):
        # 計算此筆訂單的名目價值（市價 * 數量）
        price = await self.client.get_price(symbol)
        return price * qty
