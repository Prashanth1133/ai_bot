from __future__ import annotations

import numpy as np


class VolumeHistogram:

    @staticmethod
    def build(

        prices,

        volume,

        bins=50,

    ):

        histogram, edges = np.histogram(

            prices,

            bins=bins,

            weights=volume,

        )

        centers = (

            edges[:-1]

            + edges[1:]

        ) / 2.0

        return {

            "price": centers,

            "volume": histogram,

        }