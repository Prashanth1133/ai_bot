class StablecoinTracker:

    STABLES = {

        "USDT",

        "USDC",

        "DAI",

        "FDUSD",

        "TUSD"

    }

    def is_stablecoin(self, event):

        return event.asset in self.STABLES