import numpy as np

from training.load_dataset import (
    load_dataset
)

from data.crypto_dataset import (
    CryptoDataset
)


class ProductionDataset:


    ##################################################

    def has_nan(

        self,
        data

    ):

        return (

            np.isnan(data).any()

            or

            np.isinf(data).any()

        )


    ##################################################

    def validate(

        self,
        X,
        y

    ):


        print("\n")
        print("="*60)
        print("VALIDATING DATASET")
        print("="*60)


        ######################################

        if self.has_nan(X):

            raise ValueError(

                "NaN detected in X"

            )


        ######################################

        for key in y.keys():

            if self.has_nan(

                y[key]

            ):

                raise ValueError(

                    f"NaN detected in {key}"

                )


        ######################################

        print(

            "Samples :",len(X)

        )

        print(

            "Sequence Length :",X.shape[1]

        )

        print(

            "Features :",X.shape[2]

        )


        print("\nTargets\n")


        for key in y.keys():

            print(

                key,
                y[key].shape

            )


        print("\n")
        print("="*60)
        print("DATASET VALID")
        print("="*60)
        print("\n")


    ##################################################

    def load(

        self,
        path

    ):


        print(

            "\nLoading Dataset ..."

        )


        ######################################

        data = load_dataset(

            path

        )


        ######################################

        if isinstance(

            data,
            np.ndarray

        ) and data.dtype == object:


            data = data.item()


        ######################################

        X = data["X"]

        y = data["y"]


        ######################################

        self.validate(

            X,
            y

        )


        ######################################

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