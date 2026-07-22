import pytest

from market.candles import Candle
from market.orderbook import OrderBook
from market.trades import Trade


def test_candle_creation():

    candle = Candle(
        symbol="BTCUSDT",
        open=100,
        high=105,
        low=99,
        close=103,
        volume=1000,
        timestamp=1,
    )

    assert candle.close == 103


def test_trade_creation():

    trade = Trade(
        symbol="BTCUSDT",
        trade_id=1,
        side="BUY",
        price=100,
        quantity=1,
        timestamp=1,
    )

    assert trade.side == "BUY"


def test_orderbook():

    book = OrderBook(
        symbol="BTCUSDT",
        bids=[],
        asks=[],
        timestamp=1,
    )

    assert book.symbol == "BTCUSDT"