from derivatives.engine import DerivativesEngine


class DerivativesProcessor:

    def __init__(self, bus):

        self.bus = bus

        self.engine = DerivativesEngine()

        self.previous_oi = {}

    async def on_derivatives(self, snapshot):

        previous = self.previous_oi.get(
            snapshot.symbol,
            snapshot.open_interest
        )

        result = self.engine.process(
            snapshot,
            previous
        )

        self.previous_oi[snapshot.symbol] = snapshot.open_interest

        await self.bus.publish(
            "derivatives_analysis",
            result
        )