import numpy as np


class ProductionBacktest:


    def __init__(self):


        self.equity_curve = []


    def update(

        self,
        balance

    ):


        self.equity_curve.append(

            balance

        )


    def maximum_drawdown(self):


        if len(

            self.equity_curve

        ) == 0:

            return 0


        peak = (

            self.equity_curve[0]

        )

        drawdown = 0


        for value in (

            self.equity_curve

        ):


            if value > peak:

                peak = value


            current = (

                (peak-value)

                /peak

            )


            if current > drawdown:

                drawdown = current


        return drawdown*100


    def summary(self):


        print("\n")


        print(

            "Max Drawdown :",

            round(

                self.maximum_drawdown(),

                2

            ),

            "%"

        )


        print("\n")