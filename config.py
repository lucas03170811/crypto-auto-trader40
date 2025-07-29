import os
from decimal import Decimal

BINANCE_API_KEY = os.getenv("BINANCE_API_KEY")
BINANCE_API_SECRET = os.getenv("BINANCE_API_SECRET")

# ✅ 模擬模式方便測試，正式環境設 "0"
TESTNET = bool(int(os.getenv("TESTNET", "0")))

# ✅ 每次初始下單金額（依帳戶資金可微調）
BASE_QTY = Decimal(os.getenv("BASE_QTY", "5"))

# ✅ 提高槓桿上限（建議仍需控制倉位總風險）
MAX_LEVERAGE = int(os.getenv("MAX_LEVERAGE", "20"))

# ✅ 提高最多可疊加倉位層數（追趨勢時放大獲利）
MAX_PYRAMID_LAYERS = int(os.getenv("MAX_PYRAMID_LAYERS", "6"))

# ✅ 放寬風控條件
# 若單筆部位損失達 -15%，自動縮倉（停損 or 減碼）
# 若報酬超過 +30%，考慮擴倉加碼（順勢加碼）
RISK_SHRINK_THRESHOLD = Decimal("-0.15")
RISK_GROW_THRESHOLD   = Decimal("0.30")

# ✅ 幣種篩選條件（放寬成交量門檻 + 接受更負的 funding）
FUNDING_RATE_MIN = Decimal("-0.02")          # 放寬資金費率
VOLUME_MIN_USD   = Decimal("3000000")         # 放寬成交量限制（3M）

# ✅ 擴大觀察幣池（前幾大熱門幣 + 新興高波動幣）
SYMBOL_POOL = [
    "BTCUSDT", "ETHUSDT", "SOLUSDT", "XRPUSDT", "ADAUSDT",
    "DOGEUSDT", "LINKUSDT", "AVAXUSDT", "MATICUSDT",
    "OPUSDT", "ARBUSDT", "SUIUSDT", "SEIUSDT",
    "1000PEPEUSDT", "1000BONKUSDT", "ENAUSDT", "NOTUSDT"
]

# ✅ 本地資料庫路徑
DB_PATH = os.getenv("DB_PATH", "trade_log.db")
