import numpy as np


class SequenceBuilder:

    def __init__(

        self,

        sequence_length=128

    ):

        self.sequence_length = sequence_length

    def build(

        self,

        features,
        labels

    ):

        X = []
        y = []

        for i in range(

            self.sequence_length,

            len(features)

        ):

            X.append(

                features[
                    i-self.sequence_length:i
                ]

            )

            y.append(

                labels[i]

            )

        return (

            np.array(X),

            np.array(y)

        )

    def save(

        self,

        path,
        X,
        y

    ):

        np.save(

            path,

            {

                "X": X,
                "y": y

            }

        )

    def load(

        self,

        path

    ):

        data = np.load(

            path,

            allow_pickle=True

        ).item()

        return (

            data["X"],

            data["y"]

        )