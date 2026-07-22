import numpy as np

from indicators.ema import EMA
from indicators.rsi import RSI
from indicators.macd import MACD


def test_ema():

    close = np.arange(1,101)

    ema = EMA(20).calculate(close)

    assert len(ema)==100


def test_rsi():

    close=np.arange(1,101)

    rsi=RSI().calculate(close)

    assert len(rsi)==100


def test_macd():

    close=np.arange(1,101)

    macd=MACD().calculate(close)

    assert "macd" in macd