from collections import defaultdict

from market.rolling_window import RollingWindow


class CandleManager:

    def __init__(self):

        self.windows = defaultdict(dict)

    def update(self, candle):

        symbol = candle.symbol

        interval = candle.interval

        if interval not in self.windows[symbol]:

            self.windows[symbol][interval] = RollingWindow()

        if candle.closed:

            self.windows[symbol][interval].add(candle)

    def latest(

        self,

        symbol,

        interval

    ):

        return self.windows[symbol][interval].latest()

    def previous(

        self,

        symbol,

        interval

    ):

        return self.windows[symbol][interval].previous()

    def history(

        self,

        symbol,

        interval

    ):

        return self.windows[symbol][interval].all()