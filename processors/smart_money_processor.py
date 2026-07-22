from smart_money.engine import SmartMoneyEngine


class SmartMoneyProcessor:

    def __init__(self, candle_manager, bus):

        self.candle_manager = candle_manager
        self.bus = bus

        self.engine = SmartMoneyEngine()

    async def on_candle(self, candle):

        if not candle.closed:
            return

        history = self.candle_manager.history(
            candle.symbol,
            candle.interval
        )

        result = self.engine.process(history)

        if result is not None:
            await self.bus.publish(
                "smart_money",
                result
            )

            await self.bus.publish(

                "order_blocks",

                result["order_blocks"]

            )

            await self.bus.publish(

                "liquidity",

                result["liquidity"]

            )

            await self.bus.publish(

                "fair_value_gap",

                result["fair_value_gaps"]

            )