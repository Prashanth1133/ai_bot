
from __future__ import annotations

from live.execution.live_engine import LiveExecutionEngine
from live.performance_monitor import PerformanceMonitor


class TradeManager:
    """
    Coordinates:
    - Risk checks
    - Order execution
    - Portfolio synchronization
    - Performance tracking
    """

    def __init__(
        self,
        exchange,
        risk_manager,
    ):
        self.execution = LiveExecutionEngine(
            exchange
        )

        self.performance = (
            PerformanceMonitor()
        )

        self.risk = risk_manager

    async def execute(
        self,
        signal,
        portfolio,
        market,
    ):
        """
        Execute a trade signal.
        """

        decision = self.risk.evaluate(
            trade=signal.trade,
            portfolio=portfolio,
            market=market,
            previous_open_interest=None,
            correlation=0,
            daily_loss=0,
            long=(
                signal.trade.side.upper()
                == "BUY"
            ),
        )

        if not decision.approved:
            return None

        execution = (
            await self.execution.execute(
                signal.trade
            )
        )

        if execution is not None:
            pnl = execution.get(
                "realized_pnl",
                0.0,
            )

            self.performance.record_trade(
                pnl
            )

        return execution

    async def synchronize(
        self,
        portfolio_manager,
    ):
        """
        Synchronize account and positions.
        """

        account = (
            await self.execution.executor
            .exchange.account()
        )

        portfolio_manager.update_balance(
            account["balance"],
            account["equity"],
            account["margin"],
        )

        positions = (
            await self.execution.executor
            .exchange.positions()
        )

        current = set()

        for position in positions:

            symbol = position["symbol"]

            current.add(symbol)

            portfolio_manager.update_position(
                symbol,
                position,
            )

        for symbol in list(
            portfolio_manager.positions.keys()
        ):
            if symbol not in current:
                portfolio_manager.remove_position(
                    symbol
                )

    def statistics(self):
        """
        Return performance summary.
        """

        return self.performance.summary()

