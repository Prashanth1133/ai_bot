from collections import deque

import numpy as np

from dataset.sequence import FeatureSequence


class DatasetBuilder:

    """
    Builds rolling AI sequences.
    """

    def __init__(

        self,

        sequence_length: int = 120

    ):

        self.sequence_length = sequence_length

        self.buffers = {}

    def update(

        self,

        symbol,

        timeframe,

        timestamp,

        feature_vector

    ):

        key = f"{symbol}_{timeframe}"

        if key not in self.buffers:

            self.buffers[key] = deque(

                maxlen=self.sequence_length

            )

        self.buffers[key].append(

            feature_vector

        )

        if len(self.buffers[key]) < self.sequence_length:

            return None

        array = np.asarray(

            self.buffers[key],

            dtype=np.float32

        )

        return FeatureSequence(

            symbol=symbol,

            timeframe=timeframe,

            timestamp=timestamp,

            features=array

        )