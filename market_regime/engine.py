from market_regime.trend import TrendStrength
from market_regime.volatility import VolatilityStrength
from market_regime.momentum import MomentumStrength
from market_regime.classifier import RegimeClassifier


class MarketRegimeEngine:

    def __init__(self):

        self.trend = TrendStrength()

        self.volatility = VolatilityStrength()

        self.momentum = MomentumStrength()

        self.classifier = RegimeClassifier()

    def process(self, features):

        trend = self.trend.calculate(
            features["ema20"],
            features["ema50"],
            features["ema200"]
        )

        volatility = self.volatility.calculate(
            features["atr"],
            features["close"]
        )

        momentum = self.momentum.calculate(
            features["rsi"],
            features["macd"]
        )

        return self.classifier.classify(
            trend,
            volatility,
            momentum,
            features.get("smart_money_score", 0.5)
        )