from __future__ import annotations

import asyncio
import json
from typing import Awaitable, Callable, Optional

import websockets


class WebSocketManager:

    def __init__(
        self,
        url: str,
        reconnect_delay: float = 5.0,
    ):
        self.url = url
        self.reconnect_delay = reconnect_delay

        self.websocket = None
        self.running = False

        self.message_handler: Optional[
            Callable[[dict], Awaitable[None]]
        ] = None

    def set_handler(
        self,
        handler: Callable[[dict], Awaitable[None]],
    ):
        self.message_handler = handler

    async def connect(self):

        while True:

            try:

                async with websockets.connect(
                    self.url,
                    ping_interval=20,
                    ping_timeout=20,
                ) as ws:

                    self.websocket = ws
                    self.running = True

                    async for message in ws:

                        if self.message_handler:

                            await self.message_handler(
                                json.loads(message)
                            )

            except Exception:

                self.running = False

                await asyncio.sleep(
                    self.reconnect_delay
                )

    async def send(self, payload: dict):

        if self.websocket:

            await self.websocket.send(
                json.dumps(payload)
            )

    async def close(self):

        self.running = False

        if self.websocket:

            await self.websocket.close()