from collections import defaultdict


class TimeframeAggregator:

    def __init__(self):

        self.states = defaultdict(dict)

    def update(

        self,

        symbol,

        timeframe,

        state

    ):

        self.states[symbol][timeframe] = state

    def get(

        self,

        symbol

    ):

        return self.states[symbol]