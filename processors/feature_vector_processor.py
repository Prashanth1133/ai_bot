from feature_engine.vector import FeatureVectorBuilder
from feature_engine.normalizer import FeatureNormalizer
from feature_engine.recorder import FeatureRecorder


class FeatureVectorProcessor:

    def __init__(self, bus):

        self.bus = bus

        self.builder = FeatureVectorBuilder()

        self.normalizer = FeatureNormalizer()

        self.recorder = FeatureRecorder()

    async def on_features(self, payload):

        vector = self.builder.build(

            payload["symbol"],

            payload["timeframe"],

            payload["timestamp"],

            payload["features"]

        )

        vector.values = self.normalizer.normalize(

            vector.values

        )

        self.recorder.save(

            vector

        )

        await self.bus.publish(

            "feature_vector",

            vector

        )