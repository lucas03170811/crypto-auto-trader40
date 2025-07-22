import os
from decimal import Decimal

BINANCE_API_KEY = os.getenv("BINANCE_API_KEY")
BINANCE_API_SECRET = os.getenv("BINANCE_API_SECRET")

TESTNET = bool(int(os.getenv("TESTNET", "0")))
BASE_QTY = Decimal(os.getenv("BASE_QTY", "2"))       # USDT used as margin per side
MAX_LEVERAGE = int(os.getenv("MAX_LEVERAGE", "10"))
MAX_PYRAMID_LAYERS = int(os.getenv("MAX_PYRAMID_LAYERS", "3"))

# risk modulation
RISK_SHRINK_THRESHOLD = Decimal("-0.10")  # equity draw‑down at which to cut size 20 %
RISK_GROW_THRESHOLD   = Decimal("0.20")   # equity gain at which to raise size 20 %

# screener
FUNDING_RATE_MIN = Decimal("0.000")       # positive funding preferred for longs
VOLUME_MIN_USD   = Decimal("25000000")    # 24 h USDT volume

SYMBOL_POOL = [  # initial universe
    "BTCUSDT", "ETHUSDT", "SOLUSDT", "DOGEUSDT", "PEPEUSDT", "1000BONKUSDT"
]

DB_PATH = os.getenv("DB_PATH", "trade_log.db")
