from models.market_ai import MarketAI
from models.trade_memory import TradeMemory
from models.self_learning import (
    SelfLearningAI,
)


class AIService:

    def __init__(self):

        self.market_ai = MarketAI()

        self.memory = TradeMemory()

        self.learning = SelfLearningAI(
            self.market_ai.pattern_ai,
            self.memory,
        )

    def process(self, candle):

        signal = self.market_ai.process_candle(
            candle
        )

        if signal:

            self.memory.open_trade(
                candle.symbol,
                signal.direction,
                float(candle.close),
                signal.pattern,
            )

        return signal