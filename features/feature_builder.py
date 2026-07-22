import numpy as np


class FeatureBuilder:

    """
    Builds the final feature vector
    consumed by TradingTransformer.
    """

    def build(

        self,
        candle,
        orderflow,
        orderbook

    ):

        return np.array([

            float(candle.open),
            float(candle.high),
            float(candle.low),
            float(candle.close),
            float(candle.volume),

            float(orderflow.delta),
            float(orderflow.cvd),
            float(orderflow.buy_volume),
            float(orderflow.sell_volume),

            len(orderbook.bids),
            len(orderbook.asks),

        ])