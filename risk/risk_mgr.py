from decimal import Decimal
import traceback

class RiskManager:
    def __init__(self, client, tp_pct=0.05, sl_pct=0.03):
        self.client = client
        self.entry_price_map = {}  # {symbol: {"side": "LONG", "entry": Decimal}}
        self.tp_pct = Decimal(tp_pct)
        self.sl_pct = Decimal(sl_pct)
        self.base_qty = Decimal("10")  # 預設下單數量，可根據資金改動

    async def register_entry(self, symbol, side, entry_price):
        self.entry_price_map[symbol] = {
            "side": side,
            "entry": Decimal(entry_price)
        }

    async def check_exit_conditions(self, symbol):
        try:
            if symbol not in self.entry_price_map:
                return  # 沒持倉不處理

            position = await self.client.get_position(symbol)
            if abs(position) == 0:
                if symbol in self.entry_price_map:
                    del self.entry_price_map[symbol]
                return

            current_price = await self.client.get_price(symbol)
            if current_price is None:
                return

            entry_info = self.entry_price_map[symbol]
            entry_price = entry_info["entry"]
            side = entry_info["side"]

            # 計算浮動報酬
            change = (Decimal(current_price) - entry_price) / entry_price
            if side == "SHORT":
                change = -change

            # 平倉條件
            if change >= self.tp_pct:
                print(f"[TAKE PROFIT] {symbol} +{change*100:.2f}%")
                await self.close_position(symbol, side)
                del self.entry_price_map[symbol]

            elif change <= -self.sl_pct:
                print(f"[STOP LOSS] {symbol} {change*100:.2f}%")
                await self.close_position(symbol, side)
                del self.entry_price_map[symbol]

        except Exception as e:
            print(f"[RISK CHECK ERROR] {symbol}: {e}")
            traceback.print_exc()

    async def close_position(self, symbol, side):
        qty = abs(await self.client.get_position(symbol))
        if qty == 0:
            return

        if side == "LONG":
            await self.client.open_short(symbol, qty)
        elif side == "SHORT":
            await self.client.open_long(symbol, qty)
        print(f"[EXIT] {symbol} 平倉完成（{side} 倉位）")
