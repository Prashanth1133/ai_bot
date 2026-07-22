from __future__ import annotations

from collections import defaultdict


class HeartbeatMetrics:

    def __init__(self):

        self.received = defaultdict(int)

        self.missed = defaultdict(int)

    def record(
        self,
        component: str,
    ):

        self.received[
            component
        ] += 1

    def missed_heartbeat(
        self,
        component: str,
    ):

        self.missed[
            component
        ] += 1

    def statistics(self):

        return {

            "received": dict(
                self.received
            ),

            "missed": dict(
                self.missed
            ),

        }