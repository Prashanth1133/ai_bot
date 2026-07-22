from app.logger import logger

from market.local_orderbook import LocalOrderBook

from market.orderbook import parse_depth
from market.orderbook import build_orderbook

from core.rest_client import BinanceREST


class OrderBookManager:

    def __init__(self):

        self.rest = BinanceREST()

        self.books = {}

    async def initialize(self, symbol):

        snapshot = await self.rest.orderbook_snapshot(symbol)

        book = LocalOrderBook(symbol)

        book.load_snapshot(snapshot)

        self.books[symbol] = book

        logger.success(f"{symbol} snapshot loaded")

    async def update(self, message):

        depth = parse_depth(message)

        symbol = depth["symbol"]

        if symbol not in self.books:

            await self.initialize(symbol)

        book = self.books[symbol]

        if depth["u"] <= book.last_update_id:
            return None

        if depth["U"] > book.last_update_id + 1:

            logger.warning(
                f"{symbol} lost synchronization"
            )

            await self.initialize(symbol)

            return None

        book.apply(depth)

        return build_orderbook(book)