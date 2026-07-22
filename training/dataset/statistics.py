from collections import Counter


class DatasetStatistics:

    def summarize(

        self,

        samples

    ):

        directions = Counter()

        for sample in samples:

            directions[sample.direction] += 1

        print()

        print("Dataset Summary")

        print("----------------")

        print("Samples :", len(samples))

        print("BUY :", directions[2])

        print("HOLD :", directions[1])

        print("SELL :", directions[0])

        print()