class ExchangeException(Exception):
    pass


class ConnectionError(ExchangeException):
    pass


class AuthenticationError(ExchangeException):
    pass


class OrderRejected(ExchangeException):
    pass


class InsufficientMargin(ExchangeException):
    pass


class RateLimitExceeded(ExchangeException):
    pass


class PositionNotFound(ExchangeException):
    pass


class SymbolNotFound(ExchangeException):
    pass


class OrderNotFound(ExchangeException):
    pass