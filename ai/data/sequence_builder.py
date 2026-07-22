import numpy as np


class SequenceBuilder:

    def __init__(

        self,

        sequence_length=120

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

            y.append(labels[i])

        return (

            np.asarray(X),

            np.asarray(y)

        )