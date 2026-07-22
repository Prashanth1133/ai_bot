from __future__ import annotations

import time


class TimestampProvider:

    @staticmethod
    def milliseconds():

        return int(time.time() * 1000)