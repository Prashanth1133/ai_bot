class WhaleTracker:

    WHALE_LIMIT = 1_000_000

    def detect(self, event):

        return event.usd_value >= self.WHALE_LIMIT