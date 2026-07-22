import numpy as np


class TimeframeFusion:

    def fuse(

        self,

        tf5,

        tf15,

        tf1h

    ):

        return np.concatenate(

            [

                tf5,

                tf15,

                tf1h

            ],

            axis=1

        )