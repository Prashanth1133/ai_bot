import ta


class AdvancedFeatures:

    def build(
        self,
        df
    ):

        df["rsi"] = (
            ta.momentum
            .RSIIndicator(
                df["close"]
            )
            .rsi()
        )

        df["macd"] = (
            ta.trend
            .MACD(
                df["close"]
            )
            .macd()
        )

        df["ema20"] = (
            ta.trend
            .EMAIndicator(
                df["close"],
                20
            )
            .ema_indicator()
        )

        df["ema50"] = (
            ta.trend
            .EMAIndicator(
                df["close"],
                50
            )
            .ema_indicator()
        )

        return df