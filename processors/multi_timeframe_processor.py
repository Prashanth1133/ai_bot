from multi_timeframe.engine import MultiTimeframeEngine


class MultiTimeframeProcessor:

    def __init__(self, bus):

        self.bus = bus

        self.engine = MultiTimeframeEngine()

    async def on_market_state(self, payload):

        result = self.engine.update(

            payload["symbol"],

            payload["timeframe"],

            payload["state"]

        )

        await self.bus.publish(

            "multi_timeframe",

            result

        )