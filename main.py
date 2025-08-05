import os
import asyncio
import config  # ✅ 只用這個就好，不要再用 from config import ...
from strategy.signal_generator import SignalGenerator
from risk.risk_mgr import RiskManager
from exchange.binance_client import BinanceClient

print("[DEBUG] MIN_NOTIONAL:", config.MIN_NOTIONAL)

async def main():
    print("\n[Engine] Initializing...\n")

    client = BinanceClient(config.BINANCE_API_KEY, config.BINANCE_API_SECRET)
    signal_generator = SignalGenerator(client)
    risk_mgr = RiskManager(client, config.EQUITY_RATIO_PER_TRADE)

    print("[Engine] Running scan...\n")
    filtered_symbols = await signal_generator.get_filtered_symbols(config.SYMBOL_POOL)
    print(f"[Engine] Filtered symbols: {filtered_symbols}\n")

    for symbol in filtered_symbols:
        signal = await signal_generator.generate_signal(symbol)
        pos = await client.get_position(symbol)
        print(f"[Position] {symbol}: {pos}")

        if signal in ["long", "short"] and pos == 0:
            print(f"[Trade] Entering {signal.upper()} {symbol}")
            qty = await risk_mgr.get_order_qty(symbol)
            notional = await risk_mgr.get_nominal_value(symbol, qty)

            if notional < config.MIN_NOTIONAL:
                print(f"[SKIP ORDER] {symbol} 名目價值過低：{notional:.2f} USDT（低於最低限制）\n")
                continue

            if signal == "long":
                await client.open_long(symbol, qty)
            elif signal == "short":
                await client.open_short(symbol, qty)

        else:
            print(f"[NO SIGNAL] {symbol} passed filter but no entry signal\n")

    equity = await client.get_equity()
    print(f"\n[Equity] Current equity: {equity:.2f} USDT\n")

if __name__ == "__main__":
    asyncio.run(main())
