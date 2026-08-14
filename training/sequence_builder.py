from collections import deque

import numpy as np


class SequenceBuilder:

    def __init__(self, window=120):

        self.window = window

        self.buffer = deque(maxlen=window)

    def update(self, feature_vector):

        self.buffer.append(feature_vector)

        if len(self.buffer) < self.window:
            return None

        sequence = np.asarray(
            self.buffer,
            dtype=np.float32,
        )

        return np.expand_dims(
            sequence,
            axis=0,
        )

    def create(self, features, labels=None):

        return self.update(features)