from __future__ import annotations


class ConsoleLogHandler:

    async def __call__(
        self,
        record,
    ):

        print(

            f"[{record.timestamp}] "

            f"{record.level:<8} "

            f"{record.component}: "

            f"{record.message}"
        )