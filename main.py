import asyncio
import time
from decimal import Decimal
from exchange.binance_client import BinanceClient
from strategy.filter import SymbolFilter
from strategy.trend import trend_signal
from strategy.revert import revert_signal
from engine.hedge_engine import HedgeEngine
from engine.pyramid_engine import PyramidEngine
from risk.risk_mgr import RiskManager
from config import SYMBOL_POOL


async def fetch_klines(client, symbol, interval="5m", limit=100):
    klines = await client.client.get_klines(symbol=symbol, interval=interval, limit=limit)
    import pandas as pd
    df = pd.DataFrame(klines, columns=[
        "timestamp", "open", "high", "low", "close", "volume",
        "close_time", "quote_asset_volume", "number_of_trades",
        "taker_buy_base_volume", "taker_buy_quote_volume", "ignore"])
    df = df[["open", "high", "low", "close", "volume"]].astype(float)
    return df


async def run_strategy():
    client = BinanceClient()
    risk_mgr = RiskManager()
    hedge_engine = HedgeEngine(client, risk_mgr)
    pyramid_engine = PyramidEngine(client, risk_mgr)
    symbol_filter = SymbolFilter(client)

    while True:
        try:
            approved = await symbol_filter.shortlist()
            if not approved:
                print("\n❌ 沒有符合條件的幣種，等待 60 秒重試...\n")
                await asyncio.sleep(60)
                continue

            for symbol in approved:
                df = await fetch_klines(client, symbol)
                long_t, short_t, adx = trend_signal(df)
                long_r, short_r = revert_signal(df)

                long_signal = long_t or long_r
                short_signal = short_t or short_r

                # 若兩種訊號都為 True，視為趨勢較強（也可能震盪）
                price = Decimal(str(df["close"].iloc[-1]))

                if long_signal and not short_signal:
                    await hedge_engine.close_side(symbol, "SHORT")
                    await pyramid_engine.try_add(symbol, "LONG", price)

                elif short_signal and not long_signal:
                    await hedge_engine.close_side(symbol, "LONG")
                    await pyramid_engine.try_add(symbol, "SHORT", price)

                elif long_signal and short_signal:
                    # 趨勢混合，兩邊都有可能 → 開雙向避險倉
                    await hedge_engine.open_dual(symbol)

                else:
                    await pyramid_engine.close_all(symbol, "LONG")
                    await pyramid_engine.close_all(symbol, "SHORT")

            print("✅ 一輪策略掃描完成，60 秒後重新執行...\n")
            await asyncio.sleep(60)

        except Exception as e:
            print(f"[ERROR] {e}")
            await asyncio.sleep(60)


if __name__ == "__main__":
    asyncio.run(run_strategy())
