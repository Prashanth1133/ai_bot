from models.market import OrderBook
from models.market import BookLevel

from decimal import Decimal


def parse_depth(message):

    data = message["data"]

    return {

        "symbol": data["s"],

        "U": data["U"],

        "u": data["u"],

        "pu": data["pu"],

        "b": data["b"],

        "a": data["a"]
    }


def build_orderbook(local_book):

    bids = sorted(
        local_book.bids.items(),
        reverse=True
    )

    asks = sorted(
        local_book.asks.items()
    )

    return OrderBook(

        symbol=local_book.symbol,

        update_id=local_book.last_update_id,

        bids=[
            BookLevel(price, qty)
            for price, qty in bids[:50]
        ],

        asks=[
            BookLevel(price, qty)
            for price, qty in asks[:50]
        ]
    )