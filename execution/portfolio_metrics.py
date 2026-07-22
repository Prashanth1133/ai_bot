from decimal import Decimal


class PortfolioMetrics:

    def __init__(self):

        self.total_equity = Decimal("0")

        self.total_exposure = Decimal("0")

        self.total_margin = Decimal("0")

        self.realized_pnl = Decimal("0")

        self.unrealized_pnl = Decimal("0")

    def update(self, snapshot):

        self.total_equity = snapshot.equity

        self.total_exposure = snapshot.exposure

        self.total_margin = snapshot.margin_used

        self.realized_pnl = snapshot.realized_pnl

        self.unrealized_pnl = snapshot.unrealized_pnl