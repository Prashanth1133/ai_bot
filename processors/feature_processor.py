from dataset.builder import DatasetBuilder


class FeatureProcessor:

    def __init__(

        self,

        feature_store,

        bus

    ):

        self.store = feature_store

        self.bus = bus

        self.builder = DatasetBuilder()

    async def on_closed_candle(

        self,

        candle

    ):

        if not candle.closed:

            return

        features = self.store.get(

            candle.symbol

        )

        vector = list(features.values())

        sequence = self.builder.update(

            candle.symbol,

            candle.interval,

            candle.close_time,

            vector

        )

        if sequence:

            await self.bus.publish(

                "sequence",

                sequence

            )