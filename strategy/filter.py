async def filter_symbols(client):
    all_symbols = ["BTCUSDT", "ETHUSDT", "SOLUSDT", "XRPUSDT", "ADAUSDT",
    "DOGEUSDT", "LINKUSDT", "AVAXUSDT", "MATICUSDT",
    "OPUSDT", "ARBUSDT", "SUIUSDT", "SEIUSDT",
    "1000PEPEUSDT", "1000BONKUSDT", "ENAUSDT", "NOTUSDT"]
    tradable = []

    for symbol in all_symbols:
        data = await client.get_klines(symbol)
        if data and len(data) >= 30:
            tradable.append(symbol)

    if not tradable:
        print("❌ 沒有符合條件的幣種，等待 60 秒重試...")
    return tradable
