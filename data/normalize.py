import numpy as np


class DataNormalizer:


    def normalize(

        self,
        features

    ):


        mean = (

            np.mean(

                features,
                axis=0

            )

        )


        std = (

            np.std(

                features,
                axis=0

            )

        )


        std[std == 0] = 1.0


        normalized = (

            features - mean

        ) / std


        return normalized


    def min_max(

        self,
        features

    ):


        minimum = (

            np.min(

                features,
                axis=0

            )

        )


        maximum = (

            np.max(

                features,
                axis=0

            )

        )


        denominator = (

            maximum - minimum

        )


        denominator[

            denominator == 0

        ] = 1


        normalized = (

            features - minimum

        ) / denominator


        return normalized