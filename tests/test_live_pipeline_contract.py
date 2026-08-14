import asyncio
from decimal import Decimal

import numpy as np

from app.settings import settings
from features.feature_builder import FeatureBuilder
from models.market import Candle
from models.signal import Signal
from paper_trading.executor import PaperTradeExecutor
from processors.sequence_processor import SequenceProcessor


def _candle(index):
    close = Decimal("100") + Decimal(index)
    return Candle(
        symbol="BTCUSDT", interval=settings.MODEL_TIMEFRAME,
        open_time=index, close_time=index + 1, open=close - 1,
        high=close + 1, low=close - 2, close=close,
        volume=Decimal("10"), trades=1, closed=True,
    )


def test_live_feature_vector_matches_model_input_contract():
    vector = FeatureBuilder.build_training_compatible([_candle(i) for i in range(21)])
    assert vector.shape == (settings.MODEL_INPUT_DIM,)
    assert vector.dtype == np.float32
    assert np.isfinite(vector).all()


def test_sequence_processor_keeps_symbols_independent():
    async def run():
        processor = SequenceProcessor(bus=None)
        packet = {"symbol": "BTCUSDT", "interval": settings.MODEL_TIMEFRAME,
                  "values": np.zeros(settings.MODEL_INPUT_DIM, dtype=np.float32)}
        for _ in range(settings.MODEL_SEQUENCE_LENGTH - 1):
            assert processor.prime(packet) is None
        sequence = processor.prime(packet)
        assert sequence.shape == (1, settings.MODEL_SEQUENCE_LENGTH, settings.MODEL_INPUT_DIM)
    asyncio.run(run())


def test_paper_executor_closes_long_at_take_profit(tmp_path):
    async def run():
        from paper_trading.journal import PaperTradeJournal
        executor = PaperTradeExecutor(PaperTradeJournal(tmp_path / "journal.jsonl"))
        signal = Signal(
            symbol="BTCUSDT", action="BUY", side="BUY", confidence=0.9,
            entry_price=100.0, take_profit=110.0, stop_loss=95.0,
        )
        await executor.on_signal(signal)
        trade = type("Trade", (), {"symbol": "BTCUSDT", "price": 110.0})()
        await executor.on_trade(trade)
        assert not executor.trade_manager.portfolio.positions
        assert executor.trade_manager.portfolio.closed_trades[0]["pnl"] == 10.0
    asyncio.run(run())
