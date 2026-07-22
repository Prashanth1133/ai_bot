from __future__ import annotations

import time


class ExecutionTimer:

    def __init__(self):

        self._times = {}

    def start(
        self,
        order_id: str,
    ):

        self._times[order_id] = time.perf_counter()

    def stop(
        self,
        order_id: str,
    ):

        start = self._times.pop(
            order_id,
            None,
        )

        if start is None:
            return 0.0

        return time.perf_counter() - start