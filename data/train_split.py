import numpy as np


class TrainSplit:


    def split(

        self,
        X,
        y,
        train_size=0.80,
        validation_size=0.10

    ):


        total = len(X)


        train_end = int(

            total * train_size

        )


        validation_end = int(

            total * (

                train_size +

                validation_size

            )

        )


        X_train = X[:train_end]

        y_train = {

            key: value[:train_end]

            for key, value

            in y.items()

        }


        X_validation = (

            X[

                train_end:

                validation_end

            ]

        )


        y_validation = {

            key:

            value[

                train_end:

                validation_end

            ]

            for key, value

            in y.items()

        }


        X_test = (

            X[

                validation_end:

            ]

        )


        y_test = {

            key:

            value[

                validation_end:

            ]

            for key, value

            in y.items()

        }


        return (

            X_train,
            y_train,

            X_validation,
            y_validation,

            X_test,
            y_test

        )