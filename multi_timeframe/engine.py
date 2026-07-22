from multi_timeframe.aggregator import TimeframeAggregator
from multi_timeframe.alignment import AlignmentEngine


class MultiTimeframeEngine:

    def __init__(self):

        self.store = TimeframeAggregator()

        self.alignment = AlignmentEngine()

    def update(

        self,

        symbol,

        timeframe,

        state

    ):

        self.store.update(

            symbol,

            timeframe,

            state

        )

        return self.alignment.calculate(

            self.store.get(symbol)

        )