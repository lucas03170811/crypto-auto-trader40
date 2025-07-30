import asyncio
from engine.hedge_engine import HedgeEngine
from exchange.binance_client import BinanceClient
from risk.risk_mgr import RiskManager
import config

async def main():
    client = BinanceClient()
    await client.initialize()

    risk_mgr = RiskManager(client)
    engine = HedgeEngine(client, risk_mgr)

    while True:
        try:
            await engine.run()
            await risk_mgr.update_equity()
            await asyncio.sleep(60)  # 每分鐘掃描一次
        except Exception as e:
            print(f"[ERROR] {e}")
            await asyncio.sleep(60)

if __name__ == "__main__":
    asyncio.run(main())
