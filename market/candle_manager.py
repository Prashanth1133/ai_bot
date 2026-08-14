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

        if not candle.closed:
            return

        window = self.windows[symbol][interval]

        # -------------------------------------------------
        # Prevent duplicate closed candles
        # -------------------------------------------------

        try:

            latest = window.latest()

            if (
                latest is not None
                and latest.close_time >= candle.close_time
            ):
                return

        except Exception:
            pass

        window.add(candle)

    def latest(
        self,
        symbol,
        interval
    ):
        if interval not in self.windows[symbol]:
            return None
        return self.windows[symbol][interval].latest()

    def previous(
        self,
        symbol,
        interval
    ):
        if interval not in self.windows[symbol]:
            return None
        return self.windows[symbol][interval].previous()

    def history(
        self,
        symbol,
        interval
    ):
        if interval not in self.windows[symbol]:
            return []
        return self.windows[symbol][interval].all()