import numpy as np


class EquityCurve:

    def build(

        self,

        trades,

    ):

        pnl = np.array(

            [t.pnl for t in trades]

        )

        return np.cumsum(pnl)