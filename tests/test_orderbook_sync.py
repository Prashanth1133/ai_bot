from decimal import Decimal
import pytest
from unittest.mock import AsyncMock

from features.engine import FeatureEngine
from features.feature_store import FeatureStore
from features.registry import Feature
from models.market import OrderBook, BookLevel
from core.orderbook_manager import OrderBookManager


def test_feature_engine_update_orderbook():
    store = FeatureStore()
    engine = FeatureEngine(store)

    book = OrderBook(
        symbol="BTCUSDT",
        update_id=100,
        bids=[
            BookLevel(price=Decimal("50000.0"), quantity=Decimal("2.5")),
            BookLevel(price=Decimal("49990.0"), quantity=Decimal("1.5")),
        ],
        asks=[
            BookLevel(price=Decimal("50010.0"), quantity=Decimal("1.0")),
            BookLevel(price=Decimal("50020.0"), quantity=Decimal("3.0")),
        ],
    )

    engine.update_orderbook("BTCUSDT", book)

    features = store.get("BTCUSDT")

    assert features[Feature.BID_VOLUME] == 4.0
    assert features[Feature.ASK_VOLUME] == 4.0
    assert features[Feature.IMBALANCE] == 0.0
    assert features[Feature.SPREAD] == 10.0
    assert features[Feature.MID_PRICE] == 50005.0


def test_orderbook_manager_sync_and_buffering():
    async def _test():
        manager = OrderBookManager()

        # Mock REST snapshot returning lastUpdateId = 1000
        manager.rest.orderbook_snapshot = AsyncMock(
            return_value={
                "lastUpdateId": 1000,
                "bids": [["50000.0", "1.0"]],
                "asks": [["50010.0", "1.0"]],
            }
        )

        msg1 = {
            "data": {
                "s": "BTCUSDT",
                "U": 990,
                "u": 1005,
                "pu": 980,
                "b": [["50000.0", "1.5"]],
                "a": [["50010.0", "1.5"]],
            }
        }

        ob1 = await manager.update(msg1)
        await asyncio.sleep(0.01)

        assert manager.books["BTCUSDT"].last_update_id == 1005

        # Sequential update
        msg2 = {
            "data": {
                "s": "BTCUSDT",
                "U": 1006,
                "u": 1010,
                "pu": 1005,
                "b": [["50001.0", "2.0"]],
                "a": [["50009.0", "2.0"]],
            }
        }

        ob2 = await manager.update(msg2)

        assert ob2 is not None
        assert ob2.update_id == 1010

    import asyncio
    asyncio.run(_test())
