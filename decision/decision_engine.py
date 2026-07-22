from decision.ensemble import EnsembleEngine
from decision.signal_ranker import SignalRanker
from decision.market_filter import MarketFilter
from decision.trade_validator import TradeValidator
from ai.meta.meta_engine import MetaEngine
from ai.models.inference_engine import InferenceEngine


class DecisionEngine:

    def __init__(self):

        self.ensemble = EnsembleEngine()

        self.ranker = SignalRanker()

        self.filter = MarketFilter()

        self.validator = TradeValidator()

        self.meta = MetaEngine()

        self.inference = InferenceEngine()

    def decide(

        self,

        signal,

    ):

        signal = self.ensemble.evaluate(signal)

        signal = self.meta.evaluate(
            signal
        )

        signal.ai_probability = self.inference.predict(
            signal.features
        )

        if not self.filter.allow(signal):

            return None

        if not self.validator.validate(signal):

            return None

        return signal