from __future__ import annotations

from datetime import datetime
from decimal import Decimal
from uuid import uuid4

from paper.order import PaperOrder
from paper.execution import ExecutionSimulator
from paper.slippage import SlippageModel
from paper.commission import CommissionModel
from paper.fills import Fill


class PaperEngine:

    """
    Executes simulated trades.
    """

    def __init__(self):

        self.execution = ExecutionSimulator()

        self.slippage = SlippageModel()

        self.commission = CommissionModel()

    def execute(

        self,

        trade,

        risk_decision,

    ):

        order = PaperOrder(

            order_id=str(uuid4()),

            symbol=trade.symbol,

            side=trade.side,

            quantity=trade.quantity,

            price=trade.entry_price,

            leverage=trade.leverage,

            stop_loss=risk_decision.adjusted_stop,

            take_profit=risk_decision.adjusted_target,

            created_at=datetime.utcnow(),

        )

        order.price = self.slippage.apply(

            order.price,

            order.side,

        )

        order = self.execution.execute(

            order,

            order.price,

        )

        value = order.price * order.quantity

        fee = self.commission.calculate(

            value,

        )

       fill = Fill(
            order_id=order.order_id,
            symbol=order.symbol,
            side=order.side,
            quantity=order.quantity,
            price=order.price,
            commission=fee,
            slippage=order.price - trade.entry_price,
            realized_pnl=Decimal("0"),
            timestamp=datetime.utcnow(),
        )

        # Extra attributes used by analyzer
        fill.market_regime = getattr(trade, "market_regime", "UNKNOWN")
        fill.pattern = getattr(trade, "pattern", "UNKNOWN")
        fill.news_label = getattr(trade, "news_label", "NONE")
        fill.session = getattr(trade, "session", "UNKNOWN")
        fill.confidence = getattr(trade, "confidence", 0.0)
        return fill