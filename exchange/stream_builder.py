class StreamBuilder:

    @staticmethod
    def trade(symbol: str):

        return f"{symbol.lower()}@trade"

    @staticmethod
    def depth(symbol: str):

        return f"{symbol.lower()}@depth@100ms"

    @staticmethod
    def kline(
        symbol: str,
        interval: str,
    ):

        return (
            f"{symbol.lower()}@kline_{interval}"
        )

    @staticmethod
    def mark_price(
        symbol: str,
    ):

        return (
            f"{symbol.lower()}@markPrice"
        )

    @staticmethod
    def liquidation(
        symbol: str,
    ):

        return (
            f"{symbol.lower()}@forceOrder"
        )

    @staticmethod
    def book_ticker(
        symbol: str,
    ):

        return (
            f"{symbol.lower()}@bookTicker"
        )