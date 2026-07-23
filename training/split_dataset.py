import numpy as np


class DatasetSplitter:


    @staticmethod
    def split(

        X,
        y,
        train_size=0.80

    ):


        size = len(X)


        train_index = int(

            size * train_size

        )


        X_train = X[:train_index]

        X_validation = X[train_index:]


        y_train = {}

        y_validation = {}


        for key in y:


            y_train[key] = (

                y[key][:train_index]

            )


            y_validation[key] = (

                y[key][train_index:]

            )


        return (

            X_train,
            X_validation,
            y_train,
            y_validation

        )