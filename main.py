import asyncio
import pandas as pd
from collections import defaultdict
from decimal import Decimal

from config import MAX_LEVERAGE
from exchange.binance_client import BinanceClient
from risk.risk_manager import RiskManager
from strategy.filter import SymbolFilter
from strategy.trend import trend_signal
from strategy.revert import revert_signal
from strategy.hedge_engine import HedgeEngine
from strategy.pyramid_engine import PyramidEngine

KLINE_CACHE = defaultdict(list)

async def kline_to_df(cache):
    df = pd.DataFrame(cache)
    df = df.astype({"open": float, "high": float, "low": float, "close": float})
    return df

async def main():
    client = BinanceClient()
    await client.initialize()

    try:
        risk      = RiskManager()
        hedger    = HedgeEngine(client, risk)
        pyramider = PyramidEngine(client, risk)
        screener  = SymbolFilter(client)

        while True:
            symbols = await screener.shortlist()
            if not symbols:
                print("❌ 沒有符合條件的幣種，等待 60 秒重試...")
                await asyncio.sleep(60)
                continue

            print(f"[INFO] 選出幣種：{symbols}")
            for s in symbols:
                await client.set_leverage(s, MAX_LEVERAGE)
                await hedger.open_dual(s)

            print("🟢 開始接收價格數據並進行交易...")
            async for msg in client.price_stream(symbols):
                try:
                    if msg["e"] != "kline":
                        continue

                    sym = msg["s"]
                    k   = msg["k"]
                    if not k["x"]:
                        continue  # 等待K線收盤

                    KLINE_CACHE[sym].append({
                        "open": k["o"], "high": k["h"], "low": k["l"], "close": k["c"],
                    })

                    df = await kline_to_df(KLINE_CACHE[sym][-60:])
                    long_sig, short_sig, adx_val = trend_signal(df)
                    long_rev, short_rev = revert_signal(df)
                    price = Decimal(df["close"].iloc[-1])

                    # breakout 觸發
                    hedge_state = hedger.active_hedges.get(sym)
                    if hedge_state:
                        entry = hedge_state["entry_price"]
                        trigger = abs((price - entry) / entry)

                        if trigger >= Decimal("0.005") or adx_val > 25:
                            direction = "LONG" if price > entry else "SHORT"
                            await hedger.close_side(sym, "SHORT" if direction == "LONG" else "LONG")
                            await pyramider.try_add(sym, direction, price)

                    # 每30根K線更新一次風控
                    if len(KLINE_CACHE[sym]) >= 30 and len(KLINE_CACHE[sym]) % 30 == 0:
                        equity = await client.get_account_balance()
                        risk.update_equity(equity)

                except Exception as e:
                    print(f"[ERROR] 處理價格數據時出錯: {e}")

    except Exception as e:
        print(f"[CRITICAL] 主程式發生錯誤: {e}")
    finally:
        await client.close()

if __name__ == "__main__":
    asyncio.run(main())
