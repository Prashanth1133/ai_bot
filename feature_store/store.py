class FeatureStore:

    def __init__(self):

        self.storage = {}

    def publish(self, record):

        key = (

            record.symbol,

            record.timeframe

        )

        if key not in self.storage:

            self.storage[key] = []

        self.storage[key].append(record)

    def latest(

        self,

        symbol,

        timeframe

    ):

        key = (symbol, timeframe)

        if key not in self.storage:

            return None

        return self.storage[key][-1]