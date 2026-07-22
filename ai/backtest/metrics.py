import numpy as np


class Metrics:

    def sharpe(
        self,
        returns
    ):

        return (
            np.mean(
                returns
            )
            /
            np.std(
                returns
            )
        )

    def max_drawdown(
        self,
        returns
    ):

        peak = returns[0]

        dd = 0

        for x in returns:

            if x > peak:
                peak = x

            current = (
                peak - x
            )

            dd = max(
                dd,
                current
            )

        return dd