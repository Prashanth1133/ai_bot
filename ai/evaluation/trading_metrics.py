import numpy as np


class TradingMetrics:

    def evaluate(

        self,

        trades,

    ):

        pnl = np.array(

            [t.pnl for t in trades]

        )

        wins = pnl[pnl > 0]

        losses = pnl[pnl <= 0]

        win_rate = (

            len(wins)

            /

            max(

                len(trades),

                1,

            )

        )

        profit_factor = (

            wins.sum()

            /

            abs(

                losses.sum()

            )

            if len(losses)

            else float("inf")

        )

        expectancy = pnl.mean()

        return {

            "win_rate": win_rate,

            "profit_factor": profit_factor,

            "expectancy": expectancy,

            "trades": len(trades),

        }