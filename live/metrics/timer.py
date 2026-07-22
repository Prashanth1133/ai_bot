from __future__ import annotations

import time


class Timer:

    def __init__(self):

        self.started = None

    def start(self):

        self.started = time.perf_counter()

    def stop(self):

        if self.started is None:
            return 0.0

        elapsed = (
            time.perf_counter()
            - self.started
        )

        self.started = None

        return elapsed