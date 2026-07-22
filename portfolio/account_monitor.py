from __future__ import annotations

import time


class AccountMonitor:

    def __init__(self):

        self.last_update = time.time()

    def heartbeat(self):

        self.last_update = time.time()

    def age(self):

        return time.time() - self.last_update