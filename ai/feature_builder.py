from collections import deque
import numpy as np


class FeatureBuilder:

    def __init__(self, window=100):
        self.window = window

        self.prices = {}
        self.volumes = {}
        self.cvd = {}
        self.delta = {}

    def _ensure(self, symbol):

        if symbol not in self.prices:
            self.prices[symbol] = deque(maxlen=self.window)
            self.volumes[symbol] = deque(maxlen=self.window)
            self.cvd[symbol] = deque(maxlen=self.window)
            self.delta[symbol] = deque(maxlen=self.window)

    def update(
        self,
        symbol,
        price,
        volume,
        cvd,
        delta,
    ):

        self._ensure(symbol)

        self.prices[symbol].append(float(price))
        self.volumes[symbol].append(float(volume))
        self.cvd[symbol].append(float(cvd))
        self.delta[symbol].append(float(delta))

    def ready(self, symbol):

        self._ensure(symbol)

        return len(self.prices[symbol]) >= self.window

    def build(self, symbol):

        self._ensure(symbol)

        prices = np.array(self.prices[symbol])
        volumes = np.array(self.volumes[symbol])
        cvd = np.array(self.cvd[symbol])
        delta = np.array(self.delta[symbol])

        returns = np.diff(prices)

        features = [
            prices[-1],
            prices.mean(),
            prices.std(),

            volumes[-1],
            volumes.mean(),
            volumes.std(),

            cvd[-1],
            cvd.mean(),

            delta[-1],
            delta.mean(),

            returns.mean(),
            returns.std(),

            prices.max(),
            prices.min(),

            (prices[-1] - prices[0]) / prices[0],
        ]

        return np.array(features, dtype=np.float32)