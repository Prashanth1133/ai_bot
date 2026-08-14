import asyncio
from collections import defaultdict

from logs.log_manager import orderbook_logger as logger

from market.local_orderbook import LocalOrderBook

from market.orderbook import parse_depth
from market.orderbook import build_orderbook

from core.rest_client import BinanceREST


class OrderBookManager:

    def __init__(self):

        self.rest = BinanceREST()

        self.books = {}

        self.buffers = defaultdict(list)

        self.syncing = set()

        self._initialize_tasks = {}

        self._locks = defaultdict(asyncio.Lock)

    async def initialize(self, symbol: str):
        """
        Synchronize orderbook using REST snapshot and buffered WS depth messages.
        Ensures single-flight execution per symbol via lock.
        """
        async with self._locks[symbol]:
            if symbol in self.books:
                return

            self.syncing.add(symbol)

            try:
                snapshot = await self.rest.orderbook_snapshot(symbol)

                book = LocalOrderBook(symbol)

                book.load_snapshot(snapshot)

                snapshot_id = book.last_update_id

                buffered = list(self.buffers[symbol])

                self.buffers[symbol].clear()

                synced = False

                for depth in buffered:

                    # Snapshot already contains update ``snapshot_id``.  The
                    # bridging event must cover the immediately following id.
                    if depth["u"] <= snapshot_id:
                        continue

                    if not synced:

                        if depth["U"] <= snapshot_id + 1 and depth["u"] >= snapshot_id + 1:
                            book.apply(depth)
                            synced = True

                    else:

                        # Binance Futures supplies ``pu``: the preceding final
                        # update id.  It is the authoritative continuity check.
                        if depth["pu"] != book.last_update_id:
                            logger.warning(
                                f"{symbol} lost synchronization while bootstrapping."
                            )
                            self.books.pop(symbol, None)
                            return
                        book.apply(depth)

                if buffered and not synced:
                    logger.warning(f"{symbol} could not bridge REST snapshot; retrying.")
                    self.books.pop(symbol, None)
                    return

                self.books[symbol] = book

                logger.success(f"{symbol} orderbook snapshot loaded (last_update_id: {book.last_update_id})")

            except Exception as e:

                logger.error(f"Error initializing orderbook for {symbol}: {e}")

                self.books.pop(symbol, None)

            finally:

                self.syncing.discard(symbol)

                self._initialize_tasks.pop(symbol, None)

    async def update(self, message: dict):
        """
        Process depth websocket message.
        """

        depth = parse_depth(message)

        symbol = depth["symbol"]

        if symbol in self.syncing:

            self.buffers[symbol].append(depth)

            return None

        if symbol not in self.books:

            self.buffers[symbol].append(depth)

            # Do not await REST synchronization inside the WebSocket handler.
            # It must keep receiving depth updates so initialize() can bridge
            # the REST snapshot with a contiguous buffered update.
            if symbol not in self.syncing:
                self.syncing.add(symbol)
                self._initialize_tasks[symbol] = asyncio.create_task(
                    self.initialize(symbol)
                )

            return None

        book = self.books[symbol]

        if depth["u"] <= book.last_update_id:
            return None

        if depth["pu"] != book.last_update_id:

            logger.warning(
                f"{symbol} lost synchronization (WS pu={depth['pu']}, Local={book.last_update_id}). Resynchronizing..."
            )

            self.books.pop(symbol, None)

            self.buffers[symbol].append(depth)

            await self.initialize(symbol)

            return None

        book.apply(depth)

        return build_orderbook(book)
