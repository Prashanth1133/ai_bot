from decimal import Decimal

from models.market import Candle


def parse_candle(message: dict) -> Candle:

    k = message["data"]["k"]

    return Candle(

        symbol=k["s"],

        interval=k["i"],

        open_time=k["t"],

        close_time=k["T"],

        open=Decimal(k["o"]),

        high=Decimal(k["h"]),

        low=Decimal(k["l"]),

        close=Decimal(k["c"]),

        volume=Decimal(k["v"]),

        trades=k["n"],

        closed=k["x"]

    )