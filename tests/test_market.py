from models.market import Candle, OrderBook, Trade


def test_candle_creation():

    candle = Candle(
        symbol="BTCUSDT",
        interval="5m",
        open_time=0,
        close_time=1,
        open=100,
        high=105,
        low=99,
        close=103,
        volume=1000,
        trades=1,
        closed=True,
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
        update_id=1,
        bids=[],
        asks=[],
    )

    assert book.symbol == "BTCUSDT"
