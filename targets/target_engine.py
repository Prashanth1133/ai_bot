from targets.future_return import FutureReturnTarget
from targets.volatility import FutureVolatilityTarget
from targets.reversal import ReversalTarget
from targets.liquidity import LiquiditySweepTarget


class TargetEngine:

    def __init__(self):

        self.future = FutureReturnTarget()

        self.volatility = FutureVolatilityTarget()

        self.reversal = ReversalTarget()

        self.liquidity = LiquiditySweepTarget()

    def build(

        self,

        candles,

        index

    ):

        return {

            "future_return":

                self.future.generate(

                    candles,

                    index

                ),

            "future_volatility":

                self.volatility.generate(

                    candles,

                    index

                ),

            "reversal":

                self.reversal.generate(

                    candles,

                    index

                ),

            "liquidity":

                self.liquidity.generate(

                    candles,

                    index

                )

        }