from pathlib import Path

import numpy as np


class FeatureRecorder:

    def __init__(

        self,

        directory="datasets"

    ):

        self.directory = Path(directory)

        self.directory.mkdir(

            exist_ok=True

        )

    def save(

        self,

        feature_vector

    ):

        filename = (

            self.directory

            /

            f"{feature_vector.symbol}.npy"

        )

        if filename.exists():

            previous = np.load(

                filename

            )

            data = np.vstack(

                [

                    previous,

                    feature_vector.values

                ]

            )

        else:

            data = np.asarray(

                [

                    feature_vector.values

                ]

            )

        np.save(

            filename,

            data

        )