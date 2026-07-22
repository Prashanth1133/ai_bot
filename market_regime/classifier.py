from market_regime.models import (
    MarketRegime,
    RegimeState,
)


class RegimeClassifier:

    def classify(

        self,

        trend,

        volatility,

        momentum,

        smart_money_score

    ):

        if trend > 0.8:

            regime = MarketRegime.STRONG_UPTREND

        elif trend > 0.3:

            regime = MarketRegime.WEAK_UPTREND

        elif trend < -0.8:

            regime = MarketRegime.STRONG_DOWNTREND

        elif trend < -0.3:

            regime = MarketRegime.WEAK_DOWNTREND

        elif volatility < 0.004:

            regime = MarketRegime.RANGE

        else:

            regime = MarketRegime.BREAKOUT

        confidence = min(
            1.0,
            (
                abs(trend)
                + volatility
                + abs(momentum)
                + smart_money_score
            ) / 4
        )

        return RegimeState(

            regime=regime,

            confidence=confidence,

            score=trend + momentum
        )