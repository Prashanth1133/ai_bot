import numpy as np

from data.build_dataset import (
    DatasetBuilder
)


class CombinedDatasetBuilder:


    def __init__(self):

        self.builder = (

            DatasetBuilder()

        )


    #################################################


    def load(

        self,
        csv_path

    ):

        return (

            self.builder.process(

                csv_path

            )

        )


    #################################################


    def combine(

        self,
        datasets

    ):


        X_list = []

        y_dict = None


        for X,y in datasets:


            X_list.append(

                X

            )


            if y_dict is None:

                y_dict = {

                    key:[]

                    for key in y.keys()

                }


            for key in y.keys():

                y_dict[key].append(

                    y[key]

                )


        X = np.concatenate(

            X_list,

            axis=0

        )


        for key in y_dict:

            y_dict[key] = (

                np.concatenate(

                    y_dict[key],

                    axis=0

                )

            )


        return (

            X,
            y_dict

        )


    #################################################


    def shuffle(

        self,
        X,
        y

    ):


        indices = (

            np.arange(

                len(X)

            )

        )


        np.random.shuffle(

            indices

        )


        X = X[indices]


        for key in y.keys():

            y[key] = (

                y[key][

                    indices

                ]

            )


        return (

            X,
            y

        )


    #################################################


    def information(

        self,
        X,
        y

    ):


        print("\n")

        print("="*50)

        print(

            "TOTAL DATASET :",

            len(X)

        )

        print(

            "INPUT SHAPE :",

            X.shape

        )


        for key in y.keys():

            print(

                key,

                y[key].shape

            )


        print("="*50)

        print("\n")