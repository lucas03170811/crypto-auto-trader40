import asyncio
from engine.hedge_engine import HedgeEngine
from exchange.binance_client import BinanceClient
from risk.risk_mgr import RiskManager
import config
import traceback

# ✅ 額外加入的函式：印出所有倉位
async def log_all_positions(client, symbols):
    print("\n[Positions Overview]")
    for symbol in symbols:
        try:
            pos = await client.get_position(symbol)
            if abs(pos) > 0:
                print(f"{symbol}: {'LONG' if pos > 0 else 'SHORT'} {abs(pos)}")
        except Exception as e:
            print(f"[Position ERROR] {symbol}: {e}")

async def main():
    client = BinanceClient()
    await client.initialize()

    risk_mgr = RiskManager(client)
    engine = HedgeEngine(client, risk_mgr)

    while True:
        try:
            symbols = await engine.run()
            await risk_mgr.update_equity()
            await log_all_positions(client, symbols)  # ✅ 新增：印出倉位
            await asyncio.sleep(60)
        except Exception as e:
            print(f"[ERROR] {e}")
            traceback.print_exc()  # ✅ 印出詳細錯誤
            await asyncio.sleep(60)

if __name__ == "__main__":
    asyncio.run(main())
