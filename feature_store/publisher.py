class FeaturePublisher:

    def __init__(

        self,

        store

    ):

        self.store = store

    def publish(

        self,

        record

    ):

        self.store.publish(record)