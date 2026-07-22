from portfolio.portfolio_metrics import PortfolioMetrics
from portfolio.portfolio_allocator import PortfolioAllocator
from portfolio.portfolio_optimizer import PortfolioOptimizer
from portfolio.correlation_matrix import CorrelationMatrix
from portfolio.exposure_manager import ExposureManager
from portfolio.cash_manager import CashManager
from portfolio.sector_manager import SectorManager


class PortfolioEngine:

    def __init__(self):

        self.metrics = PortfolioMetrics()

        self.allocator = PortfolioAllocator()

        self.optimizer = PortfolioOptimizer()

        self.correlation = CorrelationMatrix()

        self.exposure = ExposureManager()

        self.cash = CashManager()

        self.sectors = SectorManager()