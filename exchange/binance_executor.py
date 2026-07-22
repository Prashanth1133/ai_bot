from decimal import Decimal
from typing import Optional, Dict, Any

from exchange.binance_futures_adapter import BinanceFuturesAdapter


class BinanceExecutor:
    """
    Execution layer for Binance Futures.

    Responsibilities:
    - Validate execution requests
    - Route orders to exchange adapter
    - Cancel orders
    - Query positions
    - Query balances

    Exchange-specific logic remains inside the adapter.
    """

    def __init__(self, exchange: BinanceFuturesAdapter):
        self.exchange = exchange

    async def market_buy(
        self,
        symbol: str,
        quantity: Decimal,
    ) -> Dict[str, Any]:
        return await self.exchange.place_order(
            symbol=symbol,
            side="BUY",
            quantity=quantity,
            order_type="MARKET",
        )

    async def market_sell(
        self,
        symbol: str,
        quantity: Decimal,
    ) -> Dict[str, Any]:
        return await self.exchange.place_order(
            symbol=symbol,
            side="SELL",
            quantity=quantity,
            order_type="MARKET",
        )

    async def limit_buy(
        self,
        symbol: str,
        quantity: Decimal,
        price: Decimal,
    ) -> Dict[str, Any]:
        return await self.exchange.place_order(
            symbol=symbol,
            side="BUY",
            quantity=quantity,
            order_type="LIMIT",
            price=price,
        )

    async def limit_sell(
        self,
        symbol: str,
        quantity: Decimal,
        price: Decimal,
    ) -> Dict[str, Any]:
        return await self.exchange.place_order(
            symbol=symbol,
            side="SELL",
            quantity=quantity,
            order_type="LIMIT",
            price=price,
        )

    async def cancel_order(
        self,
        symbol: str,
        order_id: str,
    ) -> Dict[str, Any]:
        return await self.exchange.cancel_order(
            symbol=symbol,
            order_id=order_id,
        )

    async def get_position(
        self,
        symbol: str,
    ) -> Dict[str, Any]:
        return await self.exchange.get_position(symbol)

    async def get_balance(
        self,
        asset: str = "USDT",
    ):
        return await self.exchange.get_balance(asset)

    async def get_open_orders(
        self,
        symbol: Optional[str] = None,
    ):
        return await self.exchange.get_open_orders(symbol)