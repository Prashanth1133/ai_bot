class PortfolioManager:


    def __init__(self):

        self.positions = []


    def add(

        self,
        symbol,
        side,
        quantity

    ):


        self.positions.append(

            {

                "symbol":symbol,

                "side":side,

                "quantity":quantity

            }

        )


    def total(self):

        return len(

            self.positions

        )