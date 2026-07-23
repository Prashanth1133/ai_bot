import numpy as np


class TradeAnalyzer:


    def __init__(self):


        self.pnl = []

        self.confidence = []


    def update(

        self,
        pnl,
        confidence

    ):


        self.pnl.append(

            pnl

        )


        self.confidence.append(

            confidence

        )


    def average_profit(self):


        if len(self.pnl) == 0:

            return 0


        return float(

            np.mean(

                self.pnl

            )

        )


    def average_confidence(self):


        if len(

            self.confidence

        ) == 0:

            return 0


        return float(

            np.mean(

                self.confidence

            )

        )


    def summary(self):


        print("\n")


        print(

            "Average Profit :",

            round(

                self.average_profit(),

                4

            )

        )


        print(

            "Average Confidence :",

            round(

                self.average_confidence(),

                4

            )

        )


        print("\n")