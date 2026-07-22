import time


class AITrader:

    def __init__(

        self,
        ai_engine,
        trade_manager

    ):

        self.ai = ai_engine
        self.trade_manager = trade_manager

        self.last_signal = {}

    async def process(

        self,
        symbol,
        features

    ):

        result = self.ai.process(

            features

        )

        signal = result["signal"]

        confidence = result[

            "confidence"

        ]

        if confidence < 0.80:

            return None

        previous = self.last_signal.get(

            symbol

        )

        if previous == signal:

            return None

        self.last_signal[

            symbol

        ] = signal

        if signal == "BUY":

            await self.trade_manager.buy(

                symbol=symbol,

                confidence=confidence,

                tp=result[
                    "take_profit"
                ],

                sl=result[
                    "stop_loss"
                ]

            )

        elif signal == "SELL":

            await self.trade_manager.sell(

                symbol=symbol,

                confidence=confidence,

                tp=result[
                    "take_profit"
                ],

                sl=result[
                    "stop_loss"
                ]

            )

        return result