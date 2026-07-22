from decimal import Decimal
from typing import Dict, Any, Optional

from exchange.exchange_client import ExchangeClient
from exchange.exceptions import ExchangeConnectionError, ExchangeOrderError


class BinanceFuturesAdapter(ExchangeClient):
    """
    Binance Futures exchange adapter.

    Responsibilities:
    - Exchange connection abstraction
    - Account data retrieval
    - Order execution routing
    - Position queries
    - Balance queries

    API implementation can be connected later without changing upper layers.
    """

    def __init__(
        self,
        api_key: str,
        api_secret: str,
        testnet: bool = True,
    ):
        self.api_key = api_key
        self.api_secret = api_secret
        self.testnet = testnet

        self.connected = False
        self.client = None

    async def connect(self):
        try:
            # Binance SDK initialization placeholder
            # Keep exchange dependency isolated here.
            self.connected = True

        except Exception as exc:
            raise ExchangeConnectionError(
                f"Binance futures connection failed: {exc}"
            )

    async def disconnect(self):
        self.connected = False
        self.client = None

    async def get_account(self) -> Dict[str, Any]:
        self._check_connection()

        return {
            "exchange": "binance_futures",
            "connected": self.connected,
        }

    async def get_balance(self, asset: str = "USDT") -> Decimal:
        self._check_connection()

        return Decimal("0")

    async def get_position(self, symbol: str) -> Dict[str, Any]:
        self._check_connection()

        return {
            "symbol": symbol,
            "size": Decimal("0"),
            "entry_price": Decimal("0"),
            "unrealized_pnl": Decimal("0"),
        }

    async def place_order(
        self,
        symbol: str,
        side: str,
        quantity: Decimal,
        order_type: str = "MARKET",
        price: Optional[Decimal] = None,
    ) -> Dict[str, Any]:

        self._check_connection()

        try:
            return {
                "symbol": symbol,
                "side": side,
                "quantity": quantity,
                "type": order_type,
                "price": price,
                "status": "NEW",
            }

        except Exception as exc:
            raise ExchangeOrderError(
                f"Order placement failed: {exc}"
            )

    async def cancel_order(
        self,
        symbol: str,
        order_id: str,
    ) -> Dict[str, Any]:

        self._check_connection()

        return {
            "symbol": symbol,
            "order_id": order_id,
            "status": "CANCELED",
        }

    async def get_open_orders(
        self,
        symbol: Optional[str] = None,
    ):

        self._check_connection()

        return []

    def _check_connection(self):
        if not self.connected:
            raise ExchangeConnectionError(
                "Exchange is not connected"
            )