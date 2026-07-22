from decimal import Decimal

from execution.execution_context import ExecutionContext


class OrderValidator:

    def __init__(
        self,
        min_qty: Decimal = Decimal("0.0001"),
        max_qty: Decimal = Decimal("1000000"),
    ):
        self.min_qty = min_qty
        self.max_qty = max_qty

    def validate(
        self,
        context: ExecutionContext,
    ) -> bool:

        if not context.symbol:
            return False

        if context.side not in ("BUY", "SELL"):
            return False

        if context.quantity <= 0:
            return False

        if context.quantity < self.min_qty:
            return False

        if context.quantity > self.max_qty:
            return False

        if (
            context.price is not None
            and context.price <= 0
        ):
            return False

        return True