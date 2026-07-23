import numpy as np


class TrainValidationSplit:

    @staticmethod
    def split(

        X,
        y,
        train_size=0.70,
        validation_size=0.15

    ):

        total = len(X)

        train_end = int(
            total * train_size
        )

        validation_end = int(

            total *

            (

                train_size +
                validation_size

            )

        )

        X_train = X[:train_end]

        X_validation = X[
            train_end:
            validation_end
        ]

        X_test = X[
            validation_end:
        ]

        y_train = {}
        y_validation = {}
        y_test = {}

        for key in y.keys():

            y_train[key] = y[key][
                :train_end
            ]

            y_validation[key] = y[key][
                train_end:
                validation_end
            ]

            y_test[key] = y[key][
                validation_end:
            ]

        return (

            X_train,
            y_train,

            X_validation,
            y_validation,

            X_test,
            y_test

        )

    @staticmethod
    def information(

        X_train,
        X_validation,
        X_test

    ):

        print("\n")

        print("=" * 50)

        print(
            "TRAIN :",
            len(X_train)
        )

        print(
            "VALIDATION :",
            len(X_validation)
        )

        print(
            "TEST :",
            len(X_test)
        )

        print("=" * 50)

        print("\n")