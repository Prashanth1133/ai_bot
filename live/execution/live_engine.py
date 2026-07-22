from __future__ import annotations

from live.execution.order_executor import OrderExecutor


class LiveExecutionEngine:

    def __init__(

        self,

        exchange,

    ):

        self.executor = OrderExecutor(exchange)

    ##########################################################

    async def execute(

        self,

        trade,

    ):

        return await self.executor.execute(

            trade

        )