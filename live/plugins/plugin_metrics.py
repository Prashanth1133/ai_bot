from collections import defaultdict


class PluginMetrics:

    def __init__(self):

        self.loaded = defaultdict(int)

        self.failed = defaultdict(int)

    def record_loaded(self, plugin):

        self.loaded[plugin] += 1

    def record_failed(self, plugin):

        self.failed[plugin] += 1

    def statistics(self):

        return {

            "loaded": dict(self.loaded),

            "failed": dict(self.failed),

        }