class StatisticRegistry:

    def __init__(self):

        self._statistics = {}

    def register(self, statistic):

        self._statistics[
            statistic.name
        ] = statistic

    def get(self, name):

        return self._statistics.get(name)

    def update(self, statistic):

        self._statistics[
            statistic.name
        ] = statistic

    def remove(self, name):

        self._statistics.pop(name, None)

    def all(self):

        return list(
            self._statistics.values()
        )

    def clear(self):

        self._statistics.clear()