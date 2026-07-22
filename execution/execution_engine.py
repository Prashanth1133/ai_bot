from __future__ import annotations

import inspect
from decimal import Decimal
from typing import Any, Optional

from execution.execution_context import ExecutionContext
from execution.execution_result import ExecutionResult


class ExecutionEngine:
    """
    Base execution engine.

    Workflow

    Validate
        ↓
    Risk
        ↓
    Execute
        ↓
    Report
    """

    def __init__(
        self,
        executor: Any,
        validator: Optional[Any] = None,
        reporter: Optional[Any] = None,
        retry_manager: Optional[Any] = None,
    ):
        self.executor = executor
        self.validator = validator
        self.reporter = reporter
        self.retry = retry_manager

    async def execute(
        self,
        context: ExecutionContext,
        risk_result=None,
    ) -> ExecutionResult:

        if self.validator:
            validation = self.validator.validate(context)

            if inspect.isawaitable(validation):
                validation = await validation

            if not validation:
                return ExecutionResult(
                    success=False,
                    symbol=context.symbol,
                    side=context.side,
                    quantity=context.quantity,
                    price=context.price or Decimal("0"),
                    status="REJECTED",
                    message="Validation failed",
                )

        if risk_result is not None:

            approved = getattr(
                risk_result,
                "approved",
                True,
            )

            if not approved:
                return ExecutionResult(
                    success=False,
                    symbol=context.symbol,
                    side=context.side,
                    quantity=context.quantity,
                    price=context.price or Decimal("0"),
                    status="RISK_REJECTED",
                    message=getattr(
                        risk_result,
                        "reason",
                        "Risk rejection",
                    ),
                )

        async def _run():
            return await self.executor.execute(context)

        if self.retry:
            result = await self.retry.run(_run)
        else:
            result = await _run()

        if self.reporter:
            report = self.reporter.record(result)

            if inspect.isawaitable(report):
                await report

        return result