from __future__ import annotations


class MetricRegistry:

    def __init__(self):

        self._metrics = {}

    def register(
        self,
        metric,
    ):

        self._metrics[metric.name] = metric

    def update(
        self,
        name: str,
        value: float,
    ):

        metric = self._metrics.get(name)

        if metric is None:
            return

        metric.value = value

    def get(
        self,
        name: str,
    ):

        return self._metrics.get(name)

    def all(self):

        return list(self._metrics.values())

    def clear(self):

        self._metrics.clear()