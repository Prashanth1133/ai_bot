class PaperTradingEngine:

    def __init__(

        self,
        capital=10000

    ):

        self.capital = capital

        self.positions = {}

    def buy(

        self,
        symbol,
        price,
        quantity

    ):

        self.positions[

            symbol

        ] = {

            "entry": price,
            "quantity": quantity

        }

        print(

            f"[PAPER BUY] "
            f"{symbol} "
            f"{quantity} "
            f"@ {price}"

        )

    def sell(

        self,
        symbol,
        price

    ):

        if symbol not in self.positions:

            return

        pos = self.positions[

            symbol

        ]

        pnl = (

            price -
            pos["entry"]

        ) * pos["quantity"]

        self.capital += pnl

        print(

            f"[PAPER SELL] "
            f"{symbol} "
            f"PnL={pnl:.2f}"
        )

        del self.positions[

            symbol

        ]