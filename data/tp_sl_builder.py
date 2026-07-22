import numpy as np


class TPSLBuilder:

    def build(
        self,
        highs,
        lows,
        closes
    ):

        tp = []
        sl = []

        for h, l, c in zip(

            highs,
            lows,
            closes

        ):

            tp.append(

                (h - c) / c

            )

            sl.append(

                (c - l) / c

            )

        return (

            np.array(tp),

            np.array(sl)

        )