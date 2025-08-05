import os
from decimal import Decimal

# API 金鑰
BINANCE_API_KEY = os.getenv("BINANCE_API_KEY")
BINANCE_API_SECRET = os.getenv("BINANCE_API_SECRET")

# 環境參數
TESTNET = bool(int(os.getenv("TESTNET", "0")))
BASE_QTY = Decimal(os.getenv("BASE_QTY", "5"))       # 每次下單金額
MAX_LEVERAGE = int(os.getenv("MAX_LEVERAGE", "15"))
MAX_PYRAMID_LAYERS = int(os.getenv("MAX_PYRAMID_LAYERS", "6"))

# 最低名目價值（下單限制）
MIN_NOTIONAL = Decimal(os.getenv("MIN_NOTIONAL", "5"))  # ✅ 補上這一行

# 單筆倉位使用總資產百分比
EQUITY_RATIO_PER_TRADE = Decimal(os.getenv("EQUITY_RATIO_PER_TRADE", "0.03"))

# 放寬風控條件
RISK_SHRINK_THRESHOLD = Decimal("-0.15")
RISK_GROW_THRESHOLD   = Decimal("0.30")

# 放寬幣種篩選條件
FUNDING_RATE_MIN = Decimal("-0.03")
VOLUME_MIN_USD   = Decimal("3000000")

# 幣種池
SYMBOL_POOL = [
    "BTCUSDT", "ETHUSDT", "SOLUSDT", "XRPUSDT", "ADAUSDT",
    "DOGEUSDT", "LINKUSDT", "AVAXUSDT", "MATICUSDT",
    "1000PEPEUSDT", "1000BONKUSDT", "SUIUSDT", "SEIUSDT",
    "ARBUSDT", "OPUSDT", "RNDRUSDT", "NEARUSDT"
]

# 日誌資料庫
DB_PATH = os.getenv("DB_PATH", "trade_log.db")
