from portfolio.risk_manager import RiskManager
from portfolio.position_sizer import PositionSizer


class PortfolioProcessor:

    def __init__(self):

        self.risk = RiskManager()

        self.sizer = PositionSizer()

    def process(

        self,

        signal,

        account,

        confidence,

        stop_distance,

        drawdown

    ):

        approved = self.risk.approve(

            signal,

            confidence,

            drawdown

        )

        if not approved:

            return None

        quantity = self.sizer.size(

            account,

            0.01,

            stop_distance

        )

        return quantity