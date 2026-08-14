from paper_trading.executor import PaperTradeExecutor


class PaperTradingEngine:

    def __init__(self):

        self.executor = PaperTradeExecutor()

    def buy(self, symbol, price, quantity=1):

        class Signal:
            pass

        sig = Signal()
        sig.action = "BUY"
        sig.symbol = symbol
        sig.price = price
        sig.entry_price = price
        sig.quantity = quantity
        sig.confidence = 1.0
        self.executor.trade_manager.open_position(sig)

    def sell(self, symbol, price):

        class Signal:
            pass

        sig = Signal()
        sig.action = "SELL"
        sig.symbol = symbol
        sig.price = price
        sig.entry_price = price
        sig.confidence = 1.0
        self.executor.trade_manager.close_position(sig)


class PaperListener:

    def __init__(self, bus):

        self.engine = PaperTradingEngine()

        bus.subscribe(
            "trade_signal",
            self.execute
        )

    async def execute(
        self,
        signal
    ):

        price = getattr(signal, "price", None) or getattr(signal, "entry_price", None) or getattr(signal, "entry", 0)

        if signal.action == "BUY":

            self.engine.buy(
                signal.symbol,
                price,
                1
            )

        elif signal.action == "SELL":

            self.engine.sell(
                signal.symbol,
                price
            )
