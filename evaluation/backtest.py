import numpy as np


class BackTester:


    def __init__(self):

        self.balance = 10000

        self.history = []


    def update(

        self,
        profit

    ):


        self.balance += profit

        self.history.append(

            self.balance

        )


    def results(self):


        print("\n")


        print(

            "Final Balance :",

            round(

                self.balance,

                2

            )

        )


        print(

            "Total Trades :",

            len(

                self.history

            )

        )


        print("\n")


        return self.history