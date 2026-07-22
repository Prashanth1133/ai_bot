import numpy as np

from ai.dataset import DatasetBuilder


class DatasetGenerator:

    def __init__(self):

        self.dataset = DatasetBuilder()

    def process(

        self,
        candles

    ):

        for i in range(

            len(candles) - 30

        ):

            current = candles[i]

            future = candles[i + 30]

            features = [

                current.open,
                current.high,
                current.low,
                current.close,
                current.volume

            ]

            self.dataset.add(

                features,

                future.close,

                current.close

            )

        return self.dataset.export()