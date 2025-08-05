import asyncio
from strategy.signal_generator import SignalGenerator
from risk.risk_mgr import RiskManager
from exchange.binance_client import BinanceClient

from config import (
    API_KEY,
    API_SECRET,
    SYMBOLS,
    MIN_NOTIONAL,
    EQUITY_RATIO_PER_TRADE,
)

async def main():
    client = BinanceClient(API_KEY, API_SECRET)
    signal_generator = SignalGenerator(client)
    risk_mgr = RiskManager(client, EQUITY_RATIO_PER_TRADE)

    print("[Engine] Running scan...\n")

    filtered_symbols = await signal_generator.get_filtered_symbols(SYMBOLS)
    print(f"[Engine] Filtered symbols: {filtered_symbols}\n")

    for symbol in filtered_symbols:
        signal = await signal_generator.generate_signal(symbol)
        pos = await client.get_position(symbol)
        print(f"[Position] {symbol}: {pos}")

        if signal == "long" and pos == 0:
            print(f"[Trade] Entering LONG {symbol}")
            qty = await risk_mgr.get_order_qty(symbol)
            notional = await risk_mgr.get_nominal_value(symbol, qty)
            if notional < MIN_NOTIONAL:
                print(f"[SKIP ORDER] LONG {symbol} 名目價值太低: {notional:.2f} USDT（低於最低限制）")
                continue
            await client.open_long(symbol, qty)

        elif signal == "short" and pos == 0:
            print(f"[Trade] Entering SHORT {symbol}")
            qty = await risk_mgr.get_order_qty(symbol)
            notional = await risk_mgr.get_nominal_value(symbol, qty)
            if notional < MIN_NOTIONAL:
                print(f"[SKIP ORDER] SHORT {symbol} 名目價值太低: {notional:.2f} USDT（低於最低限制）")
                continue
            await client.open_short(symbol, qty)

        else:
            print(f"[NO SIGNAL] {symbol} passed filter but no entry signal\n")

    # ✅ 直接印出 equity
    equity = await client.get_equity()
    print(f"\n[Equity] Current equity: {equity:.2f} USDT\n")

if __name__ == "__main__":
    asyncio.run(main())
