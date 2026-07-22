import numpy as np

from ai.model import TradingTransformer
from ai.inference import InferenceEngine


class Backtester:

    def __init__(self):

        self.balance = 10000.0

        self.position = None

        self.trades = 0

        self.wins = 0

    def run(

        self,
        model,
        X,
        prices

    ):

        engine = InferenceEngine(

            model

        )

        for i in range(

            len(X)

        ):

            result = engine.predict(

                X[i]

            )

            signal = result[

                "signal"

            ]

            price = prices[i]

            if signal == "BUY":

                if self.position is None:

                    self.position = price

                    self.trades += 1

            elif signal == "SELL":

                if self.position is not None:

                    pnl = (

                        price -

                        self.position

                    )

                    self.balance += pnl

                    if pnl > 0:

                        self.wins += 1

                    self.position = None

        return {

            "balance": self.balance,

            "trades": self.trades,

            "wins": self.wins,

            "win_rate":

                self.wins /

                max(

                    self.trades,

                    1

                )

        }