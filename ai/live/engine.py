from ai.inference import infer
from ai.risk.manager import (
    RiskManager
)


class LiveAI:

    def __init__(self):

        self.risk = (
            RiskManager()
        )

    def process(
        self,
        features,
        price
    ):

        signal = infer(
            features
        )

        return {

            "signal":
            signal,

            "stop_loss":
            self.risk.stop_loss(
                price
            ),

            "take_profit":
            self.risk.take_profit(
                price
            )
        }