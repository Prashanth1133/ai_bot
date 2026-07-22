from feature_fusion.fusion_engine import (
    FeatureFusionEngine
)


class FeatureFusionProcessor:

    def __init__(self, bus):

        self.bus = bus

        self.engine = FeatureFusionEngine()

        self.cache = {}

    async def on_update(

        self,

        payload

    ):

        symbol = payload["symbol"]

        timeframe = payload["timeframe"]

        timestamp = payload["timestamp"]

        modules = payload["modules"]

        vector = self.engine.build(

            symbol,

            timeframe,

            timestamp,

            modules

        )

        await self.bus.publish(

            "feature_vector",

            vector

        )