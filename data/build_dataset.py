import pandas as pd

from data.feature_builder import FeatureBuilder
from data.label_builder import LabelBuilder
from data.reversal_detector import ReversalDetector
from data.market_regime import MarketRegimeBuilder
from data.confidence_builder import ConfidenceBuilder
from data.volatility_builder import VolatilityBuilder
from data.tp_sl_builder import TPSLBuilder
from data.sequence_builder import SequenceBuilder


class DatasetBuilder:

    def process(
        self,
        path
    ):

        df = pd.read_csv(path)

        prices = df["close"].values

        features = FeatureBuilder().build(
            df
        )

        direction = LabelBuilder().build(
            prices
        )

        reversal = ReversalDetector().build(
            prices
        )

        market_regime = (
            MarketRegimeBuilder()
            .build(prices)
        )

        confidence = (
            ConfidenceBuilder()
            .build(prices)
        )

        volatility = (
            VolatilityBuilder()
            .build(prices)
        )

        tp, sl = TPSLBuilder().build(

            df["high"].values,

            df["low"].values,

            prices

        )

        min_size = min(

            len(features),
            len(direction),
            len(reversal),
            len(market_regime),
            len(confidence),
            len(volatility),
            len(tp),
            len(sl)

        )

        features = features[:min_size]

        direction = direction[:min_size]

        reversal = reversal[:min_size]

        market_regime = market_regime[:min_size]

        confidence = confidence[:min_size]

        volatility = volatility[:min_size]

        tp = tp[:min_size]

        sl = sl[:min_size]

        X, _ = SequenceBuilder().build(

            features,

            direction

        )

        sequence_count = len(X)

        y = {

            "direction":
                direction[-sequence_count:],

            "reversal":
                reversal[-sequence_count:],

            "market_regime":
                market_regime[-sequence_count:],

            "confidence":
                confidence[-sequence_count:],

            "volatility":
                volatility[-sequence_count:],

            "take_profit":
                tp[-sequence_count:],

            "stop_loss":
                sl[-sequence_count:]

        }

        return X, y