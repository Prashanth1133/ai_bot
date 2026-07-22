from patterns.engine import PatternEngine


class PatternProcessor:

    def __init__(self, bus):

        self.bus = bus

        self.engine = PatternEngine()

    async def on_candle(self, candles):

        patterns = self.engine.detect(candles)

        await self.bus.publish(

            "patterns",

            patterns

        )