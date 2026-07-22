from __future__ import annotations

import numpy as np


class VolumeNodes:

    @staticmethod
    def high_volume_nodes(

        histogram,

        threshold=0.80,

    ):

        volume = histogram["volume"]

        price = histogram["price"]

        cutoff = np.max(volume) * threshold

        return [

            float(price[i])

            for i in range(len(price))

            if volume[i] >= cutoff

        ]

    @staticmethod
    def low_volume_nodes(

        histogram,

        threshold=0.20,

    ):

        volume = histogram["volume"]

        price = histogram["price"]

        cutoff = np.max(volume) * threshold

        return [

            float(price[i])

            for i in range(len(price))

            if volume[i] <= cutoff

        ]