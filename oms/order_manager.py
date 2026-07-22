from oms.order_repository import OrderRepository
from oms.order_tracker import OrderTracker
from oms.position_manager import PositionManager
from oms.fill_processor import FillProcessor
from portfolio.portfolio_engine import PortfolioEngine

class OrderManager:

    def __init__(self):

        self.repository = OrderRepository()

        self.tracker = OrderTracker()

        self.positions = PositionManager()

        self.processor = FillProcessor(

            self.repository,

            self.tracker,

            self.positions,

        )

        self.portfolio_engine = PortfolioEngine()

    def register(self, execution):

        self.repository.add(execution)

        self.tracker.register(execution)

    def completed(self, execution):

        self.processor.process(execution)