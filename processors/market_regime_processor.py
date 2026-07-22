from market_regime.engine import MarketRegimeEngine


class MarketRegimeProcessor:

    def __init__(self, bus):

        self.bus = bus

        self.engine = MarketRegimeEngine()

    async def on_features(self, features):

        regime = self.engine.process(features)

        await self.bus.publish(

            "market_regime",

            regime

        )