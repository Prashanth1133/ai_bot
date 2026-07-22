from __future__ import annotations

from collections import deque
from datetime import datetime


class ServiceEvents:

    def __init__(self):

        self.events = deque(maxlen=5000)

    def emit(
        self,
        service,
        event,
    ):

        self.events.append(
            {
                "service": service,
                "event": event,
                "timestamp": datetime.utcnow(),
            }
        )

    def history(self):

        return list(self.events)

    def latest(self):

        if not self.events:

            return None

        return self.events[-1]