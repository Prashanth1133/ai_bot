import numpy as np


class FeatureBuilder:

    """Build the same eleven price/volume features used during training."""

    @staticmethod
    def build_training_compatible(candles):
        """Return one vector for the last closed candle, or ``None`` until warm."""
        if len(candles) < 21:
            return None

        closes = np.asarray([float(item.close) for item in candles], dtype=np.float64)
        volumes = np.asarray([float(item.volume) for item in candles], dtype=np.float64)
        latest = candles[-1]
        previous_close = closes[-2]
        if previous_close <= 0:
            return None

        returns = (closes[-1] - previous_close) / previous_close

        def ema(values, span):
            alpha = 2.0 / (span + 1.0)
            weights = (1.0 - alpha) ** np.arange(len(values) - 1, -1, -1)
            return float(np.dot(weights, values) / weights.sum())

        returns_history = np.diff(closes) / closes[:-1]
        deltas = np.diff(closes)
        gains = np.maximum(deltas[-14:], 0.0)
        losses = np.maximum(-deltas[-14:], 0.0)
        rs = gains.mean() / (losses.mean() + 1e-8)
        rsi = 100.0 - (100.0 / (1.0 + rs))

        return np.asarray([
            float(latest.open), float(latest.high), float(latest.low),
            float(latest.close), float(latest.volume), returns,
            ema(closes, 10), ema(closes, 50),
            float(np.std(returns_history[-20:], ddof=1)),
            float(volumes[-20:].mean()), rsi,
        ], dtype=np.float32)


    def build(

        self,
        candle,
        orderflow,
        orderbook

    ):


        bid_volume = sum(

            float(level.quantity)

            for level

            in orderbook.bids

        )


        ask_volume = sum(

            float(level.quantity)

            for level

            in orderbook.asks

        )


        return np.array([

            #-----------------
            # OHLCV
            #-----------------

            float(candle.open),

            float(candle.high),

            float(candle.low),

            float(candle.close),

            float(candle.volume),


            #-----------------
            # ORDERFLOW
            #-----------------

            float(orderflow.delta),

            float(orderflow.cvd),

            float(orderflow.buy_volume),

            float(orderflow.sell_volume),


            #-----------------
            # ORDERBOOK
            #-----------------

            float(bid_volume),

            float(ask_volume),

        ],

        dtype=np.float32

        )
