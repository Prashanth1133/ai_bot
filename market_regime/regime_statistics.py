from collections import Counter


class RegimeStatistics:

    def __init__(self):

        self.counter = Counter()

    def update(

        self,

        snapshot,

    ):

        self.counter[
            snapshot.regime.value
        ] += 1

    def statistics(self):

        return dict(self.counter)