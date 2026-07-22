from __future__ import annotations

# import asyncio


class StrategyRunner:

    """
    Runs the existing live trading pipeline
    during backtesting.
    """

    def __init__(

        self,

        market_engine,

        risk_manager,

        execution_engine,

        portfolio,

        trade_log,

        metrics,

        analyzer,

    ):

        self.market_engine = market_engine

        self.bus = market_engine.bus

        self.risk_manager = risk_manager

        self.execution_engine = execution_engine

        self.portfolio = portfolio

        self.trade_log = trade_log

        self.metrics = metrics

        self.analyzer = analyzer

        self.latest_signal = None

        self.bus.subscribe(

            "trade_signal",

            self.on_signal,

        )

    ########################################################

    async def on_signal(

        self,

        signal,

    ):

        self.latest_signal = signal

        try:

            decision = self.risk_manager.evaluate(

                trade=signal.trade,

                portfolio=self.portfolio,

                market=signal.market,

                previous_open_interest=getattr(
                    signal,
                    "previous_open_interest",
                    None,
                ),

                correlation=getattr(
                    signal,
                    "correlation",
                    None,
                ),

                daily_loss=getattr(
                    signal,
                    "daily_loss",
                    0,
                ),

                long=signal.trade.side.upper() == "BUY",

            )

        except AttributeError:

            return

        if not decision.approved:

            return

        fill = await self.execution_engine.execute(

            signal.trade,

            decision,

        )

        if fill is None:

            return

        self.trade_log.add(fill)

        self.metrics.update(fill)

        self.analyzer.add_trade(fill)

        self.portfolio.orders.append(fill)