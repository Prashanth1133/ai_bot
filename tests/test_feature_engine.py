import numpy as np

from features.engine import FeatureEngine


def test_feature_engine():

    engine=FeatureEngine()

    candles={

        "close":np.arange(500),

        "high":np.arange(500),

        "low":np.arange(500),

        "volume":np.random.rand(500),

    }

    features=engine.process(candles)

    assert features is not None