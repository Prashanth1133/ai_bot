class FillProcessor:

    def __init__(

        self,

        repository,

        tracker,

        position_manager,

        portfolio_engine,

    ):

        self.repository = repository

        self.tracker = tracker

        self.positions = position_manager

        self.portfolio_engine = portfolio_engine

    def process(self, execution):

        self.repository.update(execution)

        self.positions.update(execution)

        self.portfolio_engine.exposure.update(

            execution.symbol,

            execution.quantity

            * execution.price,

        )

        if execution.success:

            self.tracker.remove(
                execution.order_id
            )