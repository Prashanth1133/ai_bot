import numpy as np


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