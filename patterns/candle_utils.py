from decimal import Decimal


def body(c):

    return abs(c.close - c.open)


def upper_wick(c):

    return c.high - max(c.open, c.close)


def lower_wick(c):

    return min(c.open, c.close) - c.low


def candle_range(c):

    return c.high - c.low


def bullish(c):

    return c.close > c.open


def bearish(c):

    return c.close < c.open