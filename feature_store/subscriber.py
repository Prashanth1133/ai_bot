class FeatureSubscriber:

    def __init__(

        self,

        store

    ):

        self.store = store

    def latest(

        self,

        symbol,

        timeframe

    ):

        return self.store.latest(

            symbol,

            timeframe

        )