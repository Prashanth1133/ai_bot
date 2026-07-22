from execution.execution_context import ExecutionContext


class OrderExecutor:

    def __init__(self, exchange):
        self.exchange = exchange

    async def execute(
        self,
        context: ExecutionContext,
    ):

        order_type = (
            "MARKET"
            if context.price is None
            else "LIMIT"
        )

        return await self.exchange.place_order(
            symbol=context.symbol,
            side=context.side,
            quantity=context.quantity,
            order_type=order_type,
            price=context.price,
        )