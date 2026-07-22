
from __future__ import annotations

from app.logger import logger

from decision.decision_engine import DecisionEngine
from signal_engine.engine import SignalEngine


class SignalProcessor:
    """
    Converts feature vectors into trading signals
    and publishes them onto the EventBus.
    """

    def __init__(self, bus):
        self.bus = bus

        self.engine = SignalEngine()
        self.decision_engine = DecisionEngine()

        self.signal_engine = None

    def set_engine(self, engine):
        """
        Inject a custom signal engine.
        """
        self.signal_engine = engine

    async def on_features(self, feature_vector):
        """
        Called when a new feature vector is available.
        """

        try:
            # Prefer injected engine
            engine = self.signal_engine or self.engine

            result = engine.evaluate(
                feature_vector
            )

            if result is None:
                return

            # Publish raw signal
            await self.bus.publish(
                "signal",
                result,
            )

            # Pass through decision engine
            trade_signal = (
                self.decision_engine.decide(
                    result
                )
            )

            if trade_signal is None:
                return

            await self.bus.publish(
                "trade_signal",
                trade_signal,
            )

            logger.debug(
                f"Trade signal published."
            )

        except Exception:
            logger.exception(
                "SignalProcessor failed."
            )

