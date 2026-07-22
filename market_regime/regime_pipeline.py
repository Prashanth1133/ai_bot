from market_regime.regime_snapshot import (
    RegimeSnapshot,
)


class RegimePipeline:

    def __init__(

        self,

        detector,

    ):

        self.detector = detector

    def process(

        self,

        symbol,

        timeframe,

        features,

    ):

        regime, confidence = (

            self.detector.detect(
                features
            )
        )

        return RegimeSnapshot(

            symbol=symbol,

            timeframe=timeframe,

            regime=regime,

            confidence=confidence,

            features=features,

        )