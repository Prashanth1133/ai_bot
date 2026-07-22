from ai.meta.trade_memory import TradeMemory
from ai.meta.performance_tracker import PerformanceTracker
from ai.meta.confidence_calibrator import ConfidenceCalibrator
from ai.meta.strategy_selector import StrategySelector
from ai.meta.regime_selector import RegimeSelector
from ai.meta.signal_quality import SignalQuality


class MetaEngine:

    """
    Institutional AI Supervisor.

    Monitors AI performance and
    dynamically adapts confidence.
    """

    def __init__(self):

        self.memory = TradeMemory()

        self.performance = PerformanceTracker()

        self.calibrator = ConfidenceCalibrator()

        self.strategy = StrategySelector()

        self.regime = RegimeSelector()

        self.quality = SignalQuality()

    def evaluate(

        self,

        signal,

    ):

        trades = self.memory.last(100)

        win_rate = self.performance.evaluate(
            trades
        )

        signal.confidence = (

            self.calibrator.calibrate(

                signal.confidence,

                win_rate,

            )

        )

        signal.strategy = (

            self.strategy.choose(

                signal.market_regime

            )

        )

        signal.quality = self.quality.score(
            signal
        )

        return signal

    def record(

        self,

        trade,

    ):

        self.memory.add(trade)