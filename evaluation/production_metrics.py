import numpy as np


class ProductionMetrics:
    """Small stateful metrics collector used by production evaluation."""

    def __init__(self):
        self.pnl = []
        self.confidence = []

    def update(self, pnl, confidence):
        self.pnl.append(float(pnl))
        self.confidence.append(float(confidence))

    def summary(self):
        return {
            "trades": len(self.pnl),
            "total_pnl": round(sum(self.pnl), 4),
            "win_rate": ProfitMetrics.win_rate([value > 0 for value in self.pnl]),
            "average_confidence": round(float(np.mean(self.confidence)), 4)
            if self.confidence else 0.0,
        }


class ProfitMetrics:


    @staticmethod
    def win_rate(results):


        if len(results) == 0:

            return 0


        wins = sum(results)

        total = len(results)


        return round(

            (wins/total)*100,

            2

        )


    @staticmethod
    def profit_factor(

        profits,
        losses

    ):


        if losses == 0:

            return 0


        return round(

            profits/losses,

            4

        )


    @staticmethod
    def drawdown(

        equity_curve

    ):


        if len(equity_curve) == 0:

            return 0


        peak = equity_curve[0]

        maximum = 0


        for value in equity_curve:


            if value > peak:

                peak = value


            dd = (

                peak-value

            )/peak


            maximum = max(

                maximum,

                dd

            )


        return round(

            maximum*100,

            4

        )


    @staticmethod
    def sharpe(

        returns

    ):


        returns = np.array(

            returns

        )


        if len(returns) == 0:

            return 0


        if returns.std() == 0:

            return 0


        return round(

            (

                returns.mean()

                /

                returns.std()

            ),

            4

        )


    @staticmethod
    def average_return(

        returns

    ):


        if len(returns) == 0:

            return 0


        return round(

            np.mean(

                returns

            ),

            4

        )


    @staticmethod
    def maximum_return(

        returns

    ):


        if len(returns) == 0:

            return 0


        return round(

            np.max(

                returns

            ),

            4

        )


    @staticmethod
    def minimum_return(

        returns

    ):


        if len(returns) == 0:

            return 0


        return round(

            np.min(

                returns

            ),

            4

        )
