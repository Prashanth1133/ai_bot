import numpy as np

from features.feature_builder import FeatureBuilder
from models.market import Candle
from decimal import Decimal


def test_feature_engine():

    candles = [Candle("BTCUSDT", "5m", i, i + 1, Decimal(i + 1),
                      Decimal(i + 2), Decimal(i), Decimal(i + 1),
                      Decimal("1"), 1, True) for i in range(21)]
    features=FeatureBuilder.build_training_compatible(candles)
    assert features.shape == (11,)
