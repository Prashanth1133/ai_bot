from __future__ import annotations

import numpy as np


class SlidingWindow:

    """
    Creates rolling windows for sequence models.
    """

    def __init__(

        self,

        window_size=128,

    ):

        self.window_size = window_size

    ########################################################

    def build(

        self,

        features,

        labels,

    ):

        x = []

        y = []

        for i in range(

            self.window_size,

            len(features),

        ):

            x.append(

                features[
                    i-self.window_size:i
                ]
            )

            y.append(labels[i])

        return (

            np.asarray(x),

            np.asarray(y),

        )