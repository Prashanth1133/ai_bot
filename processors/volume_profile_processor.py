from volume_profile.engine import VolumeProfileEngine


class VolumeProfileProcessor:

    def __init__(

        self,

        bus,

        candles

    ):

        self.bus = bus

        self.candles = candles

        self.engine = VolumeProfileEngine()

    async def on_candle(self, candle):

        if not candle.closed:

            return

        candles = self.candles.get(

            candle.symbol,

            candle.interval

        )

        result = self.engine.process(candles)

        await self.bus.publish(

            "volume_profile",

            result

        )