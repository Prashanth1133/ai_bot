import pytest
from unittest.mock import MagicMock, patch
from decimal import Decimal
import numpy as np

from app.settings import settings
from market.historical import BinanceHistoricalData
from processors.feature_processor import FeatureProcessor
from processors.sequence_processor import SequenceProcessor
from models.market import Candle


def test_binance_historical_data_convert():
    client = BinanceHistoricalData()
    raw_row = [
        1609459200000,  # Open time
        "29000.0",      # Open
        "29500.0",      # High
        "28800.0",      # Low
        "29300.0",      # Close
        "100.5",        # Volume
    ]
    candle = client._convert("BTCUSDT", "5m", raw_row)
    assert candle.symbol == "BTCUSDT"
    assert candle.interval == "5m"
    assert candle.open == 29000.0
    assert candle.high == 29500.0
    assert candle.low == 28800.0
    assert candle.close == 29300.0
    assert candle.volume == 100.5
    assert candle.closed is True


def test_feature_processor_build_historical_vector():
    processor = FeatureProcessor(feature_store=None, bus=None)
    
    # Generate 30 candles
    candles = []
    for i in range(30):
        c = MagicMock()
        c.closed = True
        c.interval = settings.MODEL_TIMEFRAME
        c.symbol = "BTCUSDT"
        c.open = 50000.0 + i
        c.high = 50100.0 + i
        c.low = 49900.0 + i
        c.close = 50050.0 + i
        c.volume = 10.0 + i
        candles.append(c)

    vectors = []
    for c in candles:
        v = processor.build_historical_vector(c)
        if v is not None:
            vectors.append(v)

    # First 20 candles won't produce vectors due to lookback requirements, remaining 10 should
    assert len(vectors) == 10
    assert vectors[0].shape == (settings.MODEL_INPUT_DIM,)
    assert vectors[0].dtype == np.float32


def test_sequence_processor_warmup():
    processor = SequenceProcessor(bus=None)
    vectors = [np.random.randn(settings.MODEL_INPUT_DIM).astype(np.float32) for _ in range(128)]
    
    count = processor.warmup("BTCUSDT", settings.MODEL_TIMEFRAME, vectors)
    assert count == 128
    
    key = ("BTCUSDT", settings.MODEL_TIMEFRAME)
    buffer = processor.buffers[key]
    assert len(buffer) == 128
