class PaperTrader:

    def __init__(self):

        self.balance = 10000

        self.positions = []

    def buy(
        self,
        symbol,
        price
    ):

        self.positions.append(
            {
                "symbol":
                symbol,

                "entry":
                price,
            }
        )

    def sell(
        self,
        symbol,
        price
    ):

        for pos in self.positions:

            if pos["symbol"] == symbol:

                pnl = (
                    (price - pos["entry"])
                    / pos["entry"]
                ) * 100

                print(
                    symbol,
                    pnl
                )

                self.positions.remove(
                    pos
                )

                return