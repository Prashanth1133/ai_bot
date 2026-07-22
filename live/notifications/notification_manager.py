from __future__ import annotations

import asyncio

from live.notifications.notification import Notification


class NotificationManager:

    def __init__(self):

        self.registry = None

        self.history = None

    def attach_registry(
        self,
        registry,
    ):

        self.registry = registry

    def attach_history(
        self,
        history,
    ):

        self.history = history

    async def notify(

        self,

        channel: str,

        title: str,

        message: str,

        level: str = "INFO",

        metadata=None,

    ):

        notification = Notification(

            channel=channel,

            title=title,

            message=message,

            level=level,

            metadata=metadata or {},

        )

        if self.history:

            self.history.add(notification)

        handler = self.registry.get(channel)

        if handler is not None:

            result = handler(notification)

            if asyncio.iscoroutine(result):

                await result