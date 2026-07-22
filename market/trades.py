
from decimal import Decimal

from models.market import (
    Trade,
    TradeSide,
)


def parse_trade(message: dict) -> Trade:
    """
    Parse Binance aggregate trade stream.

    Binance Payload:
    {
        "stream": "btcusdt@trade",
        "data": {
            "e": "aggTrade",
            "E": 123456789,
            "s": "BTCUSDT",
            "a": 5933014,
            "p": "50000.50",
            "q": "0.001",
            "f": 100,
            "l": 105,
            "T": 123456785,
            "m": False,
            "M": True
        }
    }
    """

    data = message.get("data", message)

    return Trade(
        symbol=data["s"],
        trade_id=int(data["t"]),
        price=Decimal(data["p"]),
        quantity=Decimal(data["q"]),
        side=(
            TradeSide.SELL
            if data["m"]
            else TradeSide.BUY
        ),
        timestamp=int(data["T"]),
        is_market_maker=bool(
            data["m"]
        ),
    )

