from __future__ import annotations


class MetricsManager:

    def __init__(self):

        self.counters = {}

        self.gauges = {}

        self.histograms = {}

    def counter(
        self,
        name: str,
    ):

        return self.counters.get(name)

    def gauge(
        self,
        name: str,
    ):

        return self.gauges.get(name)

    def histogram(
        self,
        name: str,
    ):

        return self.histograms.get(name)

    def register_counter(
        self,
        name,
        counter,
    ):

        self.counters[name] = counter

    def register_gauge(
        self,
        name,
        gauge,
    ):

        self.gauges[name] = gauge

    def register_histogram(
        self,
        name,
        histogram,
    ):

        self.histograms[name] = histogram