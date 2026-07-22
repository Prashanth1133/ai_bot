from context.context_snapshot import ContextSnapshot


class ContextBuilder:

    def __init__(

        self,

        registry,

    ):

        self.registry = registry

    def build(

        self,

        symbol,

        timeframe,

    ):

        snapshot = ContextSnapshot(

            symbol=symbol,

            timeframe=timeframe,

        )

        for _, provider in self.registry.providers():

            provider(snapshot)

        return snapshot