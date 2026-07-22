from __future__ import annotations

from decimal import Decimal

from backtest.data_loader import HistoricalDataLoader
from backtest.replay import ReplayEngine
from backtest.trade_log import TradeLog
from backtest.portfolio import BacktestPortfolio
from backtest.metrics import PerformanceMetrics
from backtest.report import BacktestReport
from backtest.analyzer import StrategyAnalyzer
from backtest.strategy_runner import StrategyRunner

from execution.execution_engine import ExecutionEngine
from execution.execution_mode import ExecutionMode
from paper.paper_engine import PaperEngine


class BacktestEngine:
    """
    Main backtesting engine.
    """

    def __init__(
        self,
        market_engine,
        feature_pipeline,
        ai_engine,
        smart_money,
        risk_manager,
        paper_engine=None,
        initial_balance=Decimal("10000"),
    ):

       self.strategy = StrategyRunner(

        market_engine=market_engine,

        risk_manager=risk_manager,

        paper_engine=self.paper_engine,

        portfolio=self.portfolio,

        trade_log=self.trade_log,

        metrics=self.metrics,

        analyzer=self.analyzer,

    )

        self.risk_manager = risk_manager

        # Use supplied PaperEngine or create one
        paper = paper_engine or PaperEngine()

        self.execution_engine = ExecutionEngine(
            mode=ExecutionMode.PAPER,
        )

        self.execution_engine.register_paper(
            paper,
        )

        self.loader = HistoricalDataLoader()

        self.replay = ReplayEngine()

        self.portfolio = BacktestPortfolio(
            balance=initial_balance
        )

        self.trade_log = TradeLog()

        self.metrics = PerformanceMetrics()

        self.analyzer = StrategyAnalyzer()

        self.report = BacktestReport()

    ########################################################

    def load_data(
        self,
        file_path,
    ):

        if file_path.endswith(".csv"):

            return self.loader.load_csv(file_path)

        elif file_path.endswith(".parquet"):

            return self.loader.load_parquet(file_path)

        raise ValueError(
            f"Unsupported file format: {file_path}"
        )

    ########################################################

    # def process_market_event(
    #     self,
    #     event,
    # ):

        decision = self.strategy.process_event(
            event
        )

        if decision is None:

            return

        risk = self.risk_manager.evaluate(

            trade=decision.trade,

            portfolio=decision.portfolio,

            market=decision.market,

            previous_open_interest=getattr(
                decision,
                "previous_open_interest",
                None,
            ),

            correlation=getattr(
                decision,
                "correlation",
                None,
            ),

            daily_loss=getattr(
                decision,
                "daily_loss",
                Decimal("0"),
            ),

            long=decision.trade.side.upper() == "BUY",

        )

        if not risk.approved:

            return

        execution = self.paper_engine.execute(

            decision.trade,

            risk,

        )

        if execution is None:

            return

        ##################################################

        self.trade_log.add(
            execution
        )

        self.metrics.update(
            execution
        )

        self.analyzer.add_trade(
            execution
        )

        ##################################################

        # Keep portfolio synchronized
        self.portfolio.orders.append(
            execution
        )

        ########################################################

        async def run(

            self,

            dataframe,

        ):

            await self.replay.replay(

                dataframe,

                self.strategy.market_engine,

            )

            return self.finish()
    ########################################################

    def finish(self):

        summary = self.analyzer.summary()

        self.report.generate(
            self.metrics
        )

        return {

            "summary": summary,

            "metrics": self.metrics,

            "portfolio": self.portfolio,

            "trades": self.trade_log.trades,

        }