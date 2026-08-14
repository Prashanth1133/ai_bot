import asyncio

from execution.execution_engine import ExecutionEngine

from models.order import Order,OrderSide,OrderType


def test_execution():

    class Executor:
        async def execute(self, context):
            return context

    engine=ExecutionEngine(Executor())

    order=Order(

        order_id="1",

        symbol="BTCUSDT",

        side=OrderSide.BUY,

        order_type=OrderType.MARKET,

        quantity=1,

    )

    # This legacy unit test only verifies delegation; the modern engine takes
    # an execution context, so use the order's compatible public fields.
    from types import SimpleNamespace
    context = SimpleNamespace(symbol=order.symbol, side=order.side, quantity=order.quantity, price=None)
    result=asyncio.run(engine.execute(context))

    assert result is not None
