import random


class MonteCarlo:

    def simulate(

        self,

        trades,

        runs=1000,

    ):

        simulations = []

        for _ in range(runs):

            sample = trades[:]

            random.shuffle(sample)

            simulations.append(sample)

        return simulations