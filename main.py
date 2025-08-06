import asyncio
import os
from decimal import Decimal
from dotenv import load_dotenv

from strategy.filter import filter_symbols
from strategy.signal_generator import generate_signal
from strategy.pyramid_engine import PyramidEngine
from exchange.binance_client import BinanceClient
from risk.risk_manager import RiskManager

# 初始化環境變數
load_dotenv()
API_KEY = os.getenv("BINANCE_API_KEY")
API_SECRET = os.getenv("BINANCE_API_SECRET")

# ✅ 最小名目價值門檻 (ex: 至少價值 $50 才允許下單)
MIN_NOTIONAL = Decimal("50")

# 主要執行邏輯
async def main():
    client = BinanceClient(API_KEY, API_SECRET)
    risk_mgr = RiskManager(client)
    pyramid = PyramidEngine(client, risk_mgr)

    while True:
        try:
            symbols = await filter_symbols(client)

            if not symbols:
                await asyncio.sleep(60)
                continue

            for symbol in symbols:
                signal = await generate_signal(symbol, client)

                if not signal:
                    continue

                price = await client.get_price(symbol)
                if price is None:
                    continue

                # 根據目前價格與設定數量計算名目價值
                notional = risk_mgr.base_qty * Decimal(price)
                if notional < MIN_NOTIONAL:
                    print(f"[SKIP] {symbol} 不符合名目價值門檻（{notional:.2f} < {MIN_NOTIONAL}）")
                    continue

                # 嘗試 pyramiding 加碼（依照方向與價格）
                await pyramid.try_add(symbol, signal.upper(), Decimal(price))

                # ✅ 檢查是否需要平倉（盈虧邏輯封裝在 RiskManager 裡）
                await risk_mgr.check_exit_conditions(symbol)

            # 每輪跑完印出帳戶淨值
            equity = await client.get_equity()
            print(f"[EQUITY] 帳戶淨值 USDT ≈ {equity:.2f}")

            await asyncio.sleep(60)  # 每 1 分鐘跑一次

        except Exception as e:
            print(f"[MAIN ERROR] {e}")

if __name__ == "__main__":
    asyncio.run(main())
