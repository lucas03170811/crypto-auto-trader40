import os
from decimal import Decimal

BINANCE_API_KEY = os.getenv("BINANCE_API_KEY")
BINANCE_API_SECRET = os.getenv("BINANCE_API_SECRET")

TESTNET = bool(int(os.getenv("TESTNET", "0")))
BASE_QTY = Decimal(os.getenv("BASE_QTY", "5"))       # 每次下單金額
MAX_LEVERAGE = int(os.getenv("MAX_LEVERAGE", "15"))
MAX_PYRAMID_LAYERS = int(os.getenv("MAX_PYRAMID_LAYERS", "5"))

# ✅ 放寬風控條件（方便初期觀察）
RISK_SHRINK_THRESHOLD = Decimal("-0.05")  # 下跌 10% 縮倉
RISK_GROW_THRESHOLD   = Decimal("0.10")   # 上漲 20% 擴倉

# ✅ 調整幣種篩選條件（放寬成交量與 funding）
FUNDING_RATE_MIN = Decimal("-0.001")       # 可接受略為負值的資金費率
VOLUME_MIN_USD   = Decimal("10000000")     # 降低為 1000 萬，增加篩選機率

# ✅ 擴大觀察幣池
SYMBOL_POOL = [
    "BTCUSDT", "ETHUSDT", "SOLUSDT", "XRPUSDT", "ADAUSDT",
    "DOGEUSDT", "LINKUSDT", "AVAXUSDT", "MATICUSDT",
    "1000PEPEUSDT", "1000BONKUSDT", "SUIUSDT", "SEIUSDT",
]

# 資料庫路徑
DB_PATH = os.getenv("DB_PATH", "trade_log.db")
