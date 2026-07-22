import numpy as np


class FutureVolatilityTarget:

    def generate(

        self,

        candles,

        index,

        horizon=20

    ):

        future = candles[index:index+horizon]

        returns = [

            (future[i].close-future[i-1].close)

            /future[i-1].close

            for i in range(1,len(future))

        ]

        return np.std(returns)