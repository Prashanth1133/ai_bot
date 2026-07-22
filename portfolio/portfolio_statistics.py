import math


class PortfolioStatistics:

    @staticmethod
    def sharpe(

        returns,

        risk_free=0.0,

    ):

        if len(returns) < 2:

            return 0.0

        avg = sum(returns) / len(returns)

        variance = sum(

            (r - avg) ** 2

            for r in returns

        ) / (len(returns) - 1)

        std = math.sqrt(variance)

        if std == 0:

            return 0.0

        return (avg - risk_free) / std