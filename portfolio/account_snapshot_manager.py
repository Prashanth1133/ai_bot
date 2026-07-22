from __future__ import annotations

from collections import deque


class AccountSnapshotManager:

    def __init__(self, size: int = 5000):

        self._snapshots = deque(maxlen=size)

    def add(self, snapshot):

        self._snapshots.append(snapshot)

    def latest(self):

        if not self._snapshots:

            return None

        return self._snapshots[-1]

    def history(self):

        return list(self._snapshots)

    def clear(self):

        self._snapshots.clear()