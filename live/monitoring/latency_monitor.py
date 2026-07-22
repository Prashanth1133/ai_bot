from __future__ import annotations

import statistics
import time
from collections import deque


class LatencyMonitor:

    def __init__(

        self,

        window=1000,

    ):

        self.samples = deque(

            maxlen=window

        )

    ##########################################################

    def record(

        self,

        latency_ms: float,

    ):

        self.samples.append(

            float(latency_ms)

        )

    ##########################################################

    def start_timer(self):

        return time.perf_counter()

    ##########################################################

    def stop_timer(

        self,

        start,

    ):

        latency = (

            time.perf_counter()

            - start

        ) * 1000

        self.record(latency)

        return latency

    ##########################################################

    @property
    def average(self):

        if not self.samples:

            return 0.0

        return statistics.mean(

            self.samples

        )

    ##########################################################

    @property
    def minimum(self):

        if not self.samples:

            return 0.0

        return min(self.samples)

    ##########################################################

    @property
    def maximum(self):

        if not self.samples:

            return 0.0

        return max(self.samples)

    ##########################################################

    @property
    def median(self):

        if not self.samples:

            return 0.0

        return statistics.median(

            self.samples

        )

    ##########################################################

    def summary(self):

        return {

            "samples": len(

                self.samples

            ),

            "average": self.average,

            "minimum": self.minimum,

            "maximum": self.maximum,

            "median": self.median,

        }