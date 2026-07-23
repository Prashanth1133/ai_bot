import numpy as np

from data.build_dataset import (
    DatasetBuilder
)

from data.crypto_dataset import (
    CryptoDataset
)


class ProductionDataset:

    def load(

        self,
        path

    ):

        # Production Dataset

        if path.endswith(".npy"):

            data = np.load(

                path,

                allow_pickle=True

            ).item()

            X = data["X"]

            y = data["y"]

        # CSV Dataset

        else:

            X, y = (

                DatasetBuilder()

                .process(

                    path

                )

            )

        dataset = (

            CryptoDataset(

                X,
                y

            )

        )

        return (

            X,
            y,
            dataset

        )