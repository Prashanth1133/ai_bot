from signal_engine.models import TradingSignal
from signal_engine.confidence import ConfidenceCalculator
from signal_engine.scorer import SignalScorer


class SignalEngine:

    def __init__(self):

        self.confidence = ConfidenceCalculator()

        self.scorer = SignalScorer()

    def generate(

        self,

        symbol,

        timeframe,

        price,

        features

    ):

        signal = self.scorer.score(features)

        confidence = self.confidence.calculate(features)

        sl = price * 0.99

        tp = price * 1.02

        reasons = [

            key

            for key, value in features.items()

            if value
        ]

        return TradingSignal(

            symbol=symbol,

            timeframe=timeframe,

            signal=signal,

            confidence=confidence,

            entry=price,

            stop_loss=sl,

            take_profit=tp,

            reasons=reasons

        )