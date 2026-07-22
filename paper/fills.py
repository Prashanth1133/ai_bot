from __future__ import annotations

from datetime import datetime


class FillEngine:

    ###########################################################

    def create_fill(

        self,

        order,

        execution_price,

        commission,

    ):

        return {

            "symbol": order.symbol,

            "side": order.side,

            "quantity": float(order.quantity),

            "price": float(execution_price),

            "stop_loss": float(order.stop_loss),

            "take_profit": float(order.take_profit),

            "commission": float(commission),

            "timestamp": datetime.utcnow(),

        }