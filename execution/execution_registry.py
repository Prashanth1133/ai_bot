from __future__ import annotations


class ExecutionRegistry:

    def __init__(self):

        self._executors = {}

    def register(
        self,
        name,
        executor,
    ):

        self._executors[name] = executor

    def get(
        self,
        name,
    ):

        return self._executors.get(name)

    def remove(
        self,
        name,
    ):

        self._executors.pop(name, None)

    def clear(self):

        self._executors.clear()

    def names(self):

        return sorted(
            self._executors.keys()
        )