from context.trend import TrendAnalyzer
from context.volatility import VolatilityAnalyzer
from context.session import SessionAnalyzer
from context.score import ContextScorer


class ContextProcessor:

    def __init__(self, bus):

        self.bus = bus

        self.trend = TrendAnalyzer()

        self.volatility = VolatilityAnalyzer()

        self.session = SessionAnalyzer()

        self.score = ContextScorer()

    async def on_features(self, features):

        context = self.score.score(

            features["trend"],

            features["volatility"],

            self.session.current()

        )

        await self.bus.publish(

            "market_context",

            context

        )