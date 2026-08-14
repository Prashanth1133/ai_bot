from app.settings import settings
from logs.log_manager import pipeline_logger

from feature_fusion.fusion_engine import FeatureFusionEngine


class FeatureFusionProcessor:

    def __init__(self, bus):

        self.bus = bus

        self.engine = FeatureFusionEngine()

        self.cache = {}

    async def on_update(self, payload):

        symbol = payload["symbol"]

        timeframe = payload["timeframe"]

        timestamp = payload["timestamp"]

        modules = payload["modules"]

        vector = self.engine.build(
            symbol,
            timeframe,
            timestamp,
            modules,
        )

        # -------------------------------------------------
        # Separate topic to prevent collision with the 11-feature model pipeline
        # -------------------------------------------------

        await self.bus.publish(
            "fused_feature_vector",
            vector,
        )