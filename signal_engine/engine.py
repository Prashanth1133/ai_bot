from signal_engine.models import TradingSignal


class SignalEngine:

    def evaluate(self, feature_vector):

        if feature_vector is None:
            return None

        confidence = 0.80

        signal = "BUY"

        return TradingSignal(

            symbol=getattr(feature_vector, "symbol", "BTCUSDT"),

            timeframe=getattr(feature_vector, "timeframe", "1m"),

            signal=signal,

            confidence=confidence,

            entry=0,

            stop_loss=0,

            take_profit=0,

            reasons=[],
        )