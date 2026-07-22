from __future__ import annotations


class ConsoleNotificationHandler:

    async def __call__(
        self,
        notification,
    ):

        print(

            f"[{notification.level}] "

            f"{notification.title}: "

            f"{notification.message}"
        )