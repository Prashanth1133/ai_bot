class Allocator:

    def allocate(
        self,
        portfolio,
        trade,
    ):
        """
        V1 allocator.

        Simply returns the quantity
        calculated by the RiskManager.
        """
        return trade.quantity


class PortfolioEngine:

    def __init__(self):

        self.allocator = Allocator()