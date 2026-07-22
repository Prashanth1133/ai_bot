from __future__ import annotations

from exchange.websocket_manager import (
    WebSocketManager,
)


class BinanceWS(WebSocketManager):

    def __init__(self):

        super().__init__(
            "wss://fstream.binance.com/stream"
        )

    async def subscribe(
        self,
        streams,
    ):

        await self.send(
            {
                "method": "SUBSCRIBE",
                "params": streams,
                "id": 1,
            }
        )

    async def unsubscribe(
        self,
        streams,
    ):

        await self.send(
            {
                "method": "UNSUBSCRIBE",
                "params": streams,
                "id": 2,
            }
        )