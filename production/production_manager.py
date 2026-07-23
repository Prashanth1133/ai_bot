from production.signal_fusion import (
    SignalFusion
)

from production.confidence_engine import (
    ConfidenceEngine
)

from production.production_decision import (
    ProductionDecision
)

from production.production_signal import (
    ProductionSignal
)

from production.market_regime_ai import (
    MarketRegimeAI
)


class ProductionManager:


    def __init__(self):


        self.fusion = (

            SignalFusion()

        )


        self.confidence = (

            ConfidenceEngine()

        )


        self.signal = (

            ProductionSignal()

        )


        self.regime = (

            MarketRegimeAI()

        )


        self.decision_engine = (

            ProductionDecision()

        )


    def evaluate(

        self,
        data

    ):


        confidence = (

            self.confidence.calculate(

                data["confidence"],

                data["sentiment"],

                data["news"],

                data["whale"]

            )

        )


        final_score = (

            self.fusion.calculate(

                data["transformer"],

                data["news"],

                data["sentiment"],

                data["social"],

                data["whale"],

                confidence

            )

        )


        signal = (

            self.fusion.decision(

                final_score

            )

        )


        regime = (

            self.regime.predict(

                data["volatility"],

                data["trend"]

            )

        )


        final_signal = (

            self.signal.generate(

                signal,

                confidence

            )

        )


        decision = (

            self.decision_engine.decide(

                final_signal,

                confidence,

                regime

            )

        )


        return {

            "signal":final_signal,

            "confidence":confidence,

            "score":final_score,

            "regime":regime,

            "decision":decision

        }