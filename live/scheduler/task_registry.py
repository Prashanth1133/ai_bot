from __future__ import annotations


class TaskRegistry:

    def __init__(self):

        self._tasks = {}

    def register(
        self,
        task,
    ):

        self._tasks[task.name] = task

    def get(
        self,
        name,
    ):

        return self._tasks.get(name)

    def remove(
        self,
        name,
    ):

        self._tasks.pop(name, None)

    def tasks(self):

        return list(self._tasks.values())

    def clear(self):

        self._tasks.clear()