from execution.execution_engine import ExecutionEngine

from models.order import Order,OrderSide,OrderType


def test_execution():

    engine=ExecutionEngine()

    order=Order(

        order_id="1",

        symbol="BTCUSDT",

        side=OrderSide.BUY,

        order_type=OrderType.MARKET,

        quantity=1,

    )

    result=engine.execute(order)

    assert result is not None