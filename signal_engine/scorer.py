from signal_engine.models import SignalType


class SignalScorer:

    def score(self, features):

        bullish = 0
        bearish = 0

        if features["bos"] == "BULLISH":
            bullish += 2

        elif features["bos"] == "BEARISH":
            bearish += 2

        if features["choch"] == "BULLISH":
            bullish += 2

        elif features["choch"] == "BEARISH":
            bearish += 2

        if features["trend"] == "BULLISH":
            bullish += 2

        elif features["trend"] == "BEARISH":
            bearish += 2

        if bullish > bearish:

            return SignalType.BUY

        if bearish > bullish:

            return SignalType.SELL

        return SignalType.HOLD