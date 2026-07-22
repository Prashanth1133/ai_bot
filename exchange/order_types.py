from enum import Enum


class OrderSide(str, Enum):

    BUY = "BUY"

    SELL = "SELL"


class OrderType(str, Enum):

    MARKET = "MARKET"

    LIMIT = "LIMIT"

    STOP = "STOP"

    STOP_MARKET = "STOP_MARKET"

    TAKE_PROFIT = "TAKE_PROFIT"

    TAKE_PROFIT_MARKET = "TAKE_PROFIT_MARKET"


class TimeInForce(str, Enum):

    GTC = "GTC"

    IOC = "IOC"

    FOK = "FOK"


class OrderStatus(str, Enum):

    NEW = "NEW"

    PARTIALLY_FILLED = "PARTIALLY_FILLED"

    FILLED = "FILLED"

    CANCELLED = "CANCELLED"

    REJECTED = "REJECTED"

    EXPIRED = "EXPIRED"