from __future__ import annotations

from types import SimpleNamespace

from paper.execution import PaperExecution


class PaperEngine:
    """Compatibility facade for legacy callers of the paper execution path."""

    def __init__(self):
        self.execution = PaperExecution()

    def execute(self, trade, risk_decision):
        normalized_trade = SimpleNamespace(
            symbol=trade.symbol,
            side=trade.side,
            quantity=trade.quantity,
            entry_price=trade.entry_price,
            stop_loss=risk_decision.adjusted_stop,
            take_profit=risk_decision.adjusted_target,
        )
        return self.execution.execute(normalized_trade)
