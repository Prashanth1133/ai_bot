class PaperOrder:


    def __init__(

        self,
        symbol,
        side,
        price,
        quantity

    ):


        self.symbol = symbol

        self.side = side

        self.price = price

        self.quantity = quantity


    def value(self):


        return (

            self.price *

            self.quantity

        )


    def display(self):


        print(

            self.symbol,

            self.side,

            self.price,

            self.quantity

        )