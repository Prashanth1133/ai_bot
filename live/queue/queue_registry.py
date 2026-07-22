from __future__ import annotations


class QueueRegistry:

    def __init__(self):

        self._queues = {}

    def register(
        self,
        name,
        queue,
    ):

        self._queues[name] = queue

    def get(
        self,
        name,
    ):

        return self._queues.get(name)

    def remove(
        self,
        name,
    ):

        self._queues.pop(name, None)

    def queues(self):

        return dict(self._queues)

    def clear(self):

        self._queues.clear()