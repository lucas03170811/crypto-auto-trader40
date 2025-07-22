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

KLINE_CACHE = defaultdict(list)  # symbol -> list[dict]

async def kline_to_df(cache):
    df = pd.DataFrame(cache)
    df = df.astype({"open":float,"high":float,"low":float,"close":float})
    return df

async def main():
    client   = BinanceClient()
    await client.initialize()

    risk     = RiskManager()
    hedger   = HedgeEngine(client, risk)
    pyramider= PyramidEngine(client, risk)
    screener = SymbolFilter(client)

    symbols = await screener.shortlist()
    for s in symbols:
        await client.set_leverage(s, MAX_LEVERAGE)
        await hedger.open_dual(s)

    async for msg in client.price_stream(symbols):
        if msg["e"] != "kline":
            continue

        sym = msg["s"]
        k   = msg["k"]

        if not k["x"]:  # closed candle only
            continue

        KLINE_CACHE[sym].append({
            "open": k["o"], "high": k["h"], "low": k["l"], "close": k["c"],
        })
        df = await kline_to_df(KLINE_CACHE[sym][-60:])  # last 60 mins
        long_sig, short_sig, adx_val = trend_signal(df)
        long_rev, short_rev          = revert_signal(df)
        price = Decimal(df["close"].iloc[-1])

        # breakout logic
        hedge_state = hedger.active_hedges.get(sym)
        if hedge_state:
            entry   = hedge_state["entry_price"]
            trigger = abs((price - entry) / entry)

            if trigger >= Decimal("0.005") or adx_val > 25:
                direction = "LONG" if price > entry else "SHORT"
                await hedger.close_side(sym, "SHORT" if direction == "LONG" else "LONG")
                await pyramider.try_add(sym, direction, price)

        # risk modulation every 30 closed candles (~30 min)
        if len(KLINE_CACHE[sym]) % 30 == 0:
            equity = await client.get_account_balance()
            risk.update_equity(equity)

if __name__ == "__main__":
    asyncio.run(main())
await client.client.close()
