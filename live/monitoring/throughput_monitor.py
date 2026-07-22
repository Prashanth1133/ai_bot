from __future__ import annotations

import time


class ThroughputMonitor:

    def __init__(self):

        self.start = time.time()

        self.events = 0

    ##########################################################

    def increment(

        self,

        count=1,

    ):

        self.events += count

    ##########################################################

    @property
    def elapsed(self):

        return max(

            time.time()

            - self.start,

            1e-9,

        )

    ##########################################################

    @property
    def eps(self):

        return (

            self.events

            / self.elapsed

        )

    ##########################################################

    def reset(self):

        self.start = time.time()

        self.events = 0

    ##########################################################

    def summary(self):

        return {

            "events": self.events,

            "seconds": self.elapsed,

            "eps": self.eps,

        }