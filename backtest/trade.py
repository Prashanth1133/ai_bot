class Trade:


    def __init__(

        self,
        side,
        entry,
        exit_price,
        quantity

    ):


        self.side = side

        self.entry = entry

        self.exit_price = exit_price

        self.quantity = quantity


    def pnl(self):


        if self.side == "BUY":

            return (

                (

                    self.exit_price -

                    self.entry

                )

                *

                self.quantity

            )


        return (

            (

                self.entry -

                self.exit_price

            )

            *

            self.quantity

        )