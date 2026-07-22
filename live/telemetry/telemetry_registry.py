class TelemetryRegistry:

    def __init__(self):

        self._records = {}

    def update(self, record):

        self._records[
            (record.component, record.metric)
        ] = record

    def get(self, component, metric):

        return self._records.get(
            (component, metric)
        )

    def all(self):

        return list(
            self._records.values()
        )

    def clear(self):

        self._records.clear()