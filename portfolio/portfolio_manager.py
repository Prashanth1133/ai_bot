from __future__ import annotations

from portfolio.capital import CapitalManager
from portfolio.exposure import ExposureManager
from portfolio.pnl import PnLManager
from portfolio.statistics import PortfolioStatistics


class PortfolioManager:

    def __init__(
        self,
        capital: CapitalManager,
    ):

        self.capital = capital

        self.exposure = ExposureManager()

        self.pnl = PnLManager()

        self.statistics = PortfolioStatistics()

    @property
    def equity(self):

        return (
            self.capital.cash
            + self.pnl.total()
        )

    def record_trade(
        self,
        pnl,
    ):

        self.statistics.add_trade(pnl)