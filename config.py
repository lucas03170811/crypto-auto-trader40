import os
from decimal import Decimal

BINANCE_API_KEY = os.getenv("BINANCE_API_KEY")
BINANCE_API_SECRET = os.getenv("BINANCE_API_SECRET")

TESTNET = bool(int(os.getenv("TESTNET", "0")))
BASE_QTY = Decimal(os.getenv("BASE_QTY", "5"))       # 每次下單金額
MAX_LEVERAGE = int(os.getenv("MAX_LEVERAGE", "15"))
MAX_PYRAMID_LAYERS = int(os.getenv("MAX_PYRAMID_LAYERS", "6"))

# ✅ 放寬風控條件
RISK_SHRINK_THRESHOLD = Decimal("-0.15")
RISK_GROW_THRESHOLD   = Decimal("0.30")

# ✅ 放寬幣種篩選條件
FUNDING_RATE_MIN = Decimal("-0.03")
VOLUME_MIN_USD   = Decimal("3000000")

SYMBOL_POOL = [
    "BTCUSDT", "ETHUSDT", "SOLUSDT", "XRPUSDT", "ADAUSDT",
    "DOGEUSDT", "LINKUSDT", "AVAXUSDT", "MATICUSDT",
    "1000PEPEUSDT", "1000BONKUSDT", "SUIUSDT", "SEIUSDT",
    "ARBUSDT", "OPUSDT", "RNDRUSDT", "NEARUSDT"
]

DB_PATH = os.getenv("DB_PATH", "trade_log.db")
