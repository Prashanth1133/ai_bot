from __future__ import annotations

from live.logging.log_record import LogRecord


class LiveLogger:

    def __init__(self):

        self.handlers = []

    def add_handler(
        self,
        handler,
    ):

        self.handlers.append(handler)

    async def log(

        self,

        level,

        component,

        message,

        metadata=None,

    ):

        record = LogRecord(

            level=level,

            component=component,

            message=message,

            metadata=metadata or {},

        )

        for handler in self.handlers:

            await handler(record)