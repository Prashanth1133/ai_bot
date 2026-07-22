class StrategyPipeline:

    def __init__(

        self,

        manager,

        signal_filter,

        selector,

    ):

        self.manager = manager

        self.signal_filter = signal_filter

        self.selector = selector

    def run(

        self,

        context,

    ):

        signals = self.manager.execute(context)

        signals = self.signal_filter.filter(signals)

        return self.selector.select(signals)