from __future__ import annotations

import json

import websockets


class UserStream:

    def __init__(self):

        self.websocket = None

        self.callback = None

    async def connect(
        self,
        listen_key: str,
    ):

        url = (
            "wss://fstream.binance.com/ws/"
            f"{listen_key}"
        )

        async with websockets.connect(url) as ws:

            self.websocket = ws

            async for message in ws:

                if self.callback:

                    await self.callback(
                        json.loads(message)
                    )

    def on_message(
        self,
        callback,
    ):

        self.callback = callback