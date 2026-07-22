class BacktestEngine:

    def __init__(self):

        self.balance = 10000

        self.position = None

        self.trades = []

    def execute(
        self,
        signal,
        price
    ):

        if signal == "BUY":

            self.position = price

        elif signal == "SELL":

            if self.position:

                pnl = (
                    (price - self.position)
                    / self.position
                ) * 100

                self.trades.append(pnl)

                self.position = None

    def stats(self):

        wins = len(
            [x for x in self.trades if x > 0]
        )

        losses = len(
            [x for x in self.trades if x <= 0]
        )

        return {
            "trades":
            len(self.trades),

            "wins":
            wins,

            "losses":
            losses,

            "win_rate":
            (
                wins /
                max(
                    1,
                    len(self.trades)
                )
            ) * 100,

            "profit":
            sum(self.trades),
        }