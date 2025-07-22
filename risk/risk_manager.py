from decimal import Decimal
from config import BASE_QTY, RISK_SHRINK_THRESHOLD, RISK_GROW_THRESHOLD, MAX_PYRAMID_LAYERS

class RiskManager:
    """Dynamically adjusts position sizing based on equity changes."""

    def __init__(self):
        self.base_qty = BASE_QTY
        self.max_layers = MAX_PYRAMID_LAYERS
        self.start_equity: Decimal | None = None

    def update_equity(self, equity: Decimal):
        if self.start_equity is None:
            self.start_equity = equity
            return

        change = (equity - self.start_equity) / self.start_equity
        if change <= RISK_SHRINK_THRESHOLD:
            self.base_qty *= Decimal("0.8")
            self.max_layers = max(1, self.max_layers - 1)
            self.start_equity = equity  # reset anchor
            print(f"[RISK] Shrink base_qty to {self.base_qty}")
        elif change >= RISK_GROW_THRESHOLD:
            self.base_qty *= Decimal("1.2")
            self.max_layers += 1
            self.start_equity = equity
            print(f"[RISK] Grow  base_qty to {self.base_qty}")
