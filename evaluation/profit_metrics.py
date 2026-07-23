import numpy as np


class ProfitMetrics:


    @staticmethod
    def win_rate(results):


        wins = sum(results)

        total = len(results)

        return wins/total


    @staticmethod
    def profit_factor(


        profits,
        losses

    ):


        if losses == 0:

            return 0


        return (

            profits/

            losses

        )


    @staticmethod
    def drawdown(


        equity_curve

    ):


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


        return maximum


    @staticmethod
    def sharpe(


        returns

    ):


        returns = np.array(

            returns

        )


        if returns.std() == 0:

            return 0


        return (

            returns.mean()

            /

            returns.std()

        )