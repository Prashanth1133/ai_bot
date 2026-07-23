import numpy as np


class MergeDataset:


    @staticmethod
    def merge(


        datasets

    ):


        X = []

        labels = []


        for data in datasets:

            X.append(

                data[0]

            )

            labels.append(

                data[1]

            )


        final_x = np.concatenate(

            X,

            axis=0

        )


        final_labels = {}


        keys = labels[0].keys()


        for key in keys:


            final_labels[key] = (

                np.concatenate(

                    [

                        label[key]

                        for label

                        in labels

                    ],

                    axis=0

                )

            )


        return (

            final_x,

            final_labels

        )