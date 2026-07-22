from __future__ import annotations

from decimal import Decimal

from paper.order import PaperOrder
from paper.fills import FillEngine
from paper.slippage import SlippageModel
from paper.commission import CommissionModel


class PaperExecution:

    def __init__(self):

        self.slippage = SlippageModel()

        self.commission = CommissionModel()

        self.fills = FillEngine()

    ###########################################################

    def execute(

        self,

        trade,

        orderbook=None,

    ):

        order = PaperOrder(

            symbol=trade.symbol,

            side=trade.side,

            quantity=Decimal(str(trade.quantity)),

            price=Decimal(str(trade.entry_price)),

            stop_loss=Decimal(str(trade.stop_loss)),

            take_profit=Decimal(str(trade.take_profit)),

        )

        execution_price = self.slippage.apply(

            order.price,

            order.side,

            orderbook,

        )

        commission = self.commission.calculate(

            execution_price,

            order.quantity,

        )

        fill = self.fills.create_fill(

            order,

            execution_price,

            commission,

        )

        return fill