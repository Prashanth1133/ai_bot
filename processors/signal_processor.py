from __future__ import annotations

from app.logger import logger
from logs.log_manager import ai_logger, pipeline_logger

from decision.decision_engine import DecisionEngine
from live.signal_engine import LiveSignalEngine


class SignalProcessor:

    def __init__(self, bus):

        self.bus = bus

        # -------------------------------------------------
        # REAL PRODUCTION AI ENGINE
        # -------------------------------------------------
        self.engine = LiveSignalEngine()

        self.decision_engine = DecisionEngine()

        # Optional external engine override
        self.signal_engine = None

    # -----------------------------------------------------
    # Optional engine override
    # -----------------------------------------------------

    def set_engine(self, engine):
        self.signal_engine = engine

    # -----------------------------------------------------
    # AI inference
    # -----------------------------------------------------

    async def on_features(self, sequence_packet):

        try:

            engine = self.signal_engine or self.engine

            symbol = sequence_packet["symbol"]

            sequence = sequence_packet["values"]

            # -------------------------------------------------
            # AI INPUT
            # -------------------------------------------------

            ai_logger.info(
                f"[AI INPUT] "
                f"{symbol} "
                f"sequence_length={len(sequence)} "
                f"features={len(sequence[-1]) if len(sequence) > 0 else 0}"
            )

            # -------------------------------------------------
            # REAL AI INFERENCE
            # -------------------------------------------------

            result = engine.evaluate(
                sequence,
                symbol=symbol,
            )

            # -------------------------------------------------
            # AI FILTERED
            # -------------------------------------------------

            if result is None:

                ai_logger.info(
                    f"[AI RESULT] "
                    f"{symbol} "
                    f"FILTERED"
                )

                return

            # -------------------------------------------------
            # AI FIRED
            # -------------------------------------------------

            ai_logger.success(
                f"[AI FIRED] "
                f"{symbol} "
                f"ACTION={result.action} "
                f"CONFIDENCE={result.confidence:.4f}"
            )

            # -------------------------------------------------
            # RAW AI SIGNAL
            # -------------------------------------------------

            await self.bus.publish(
                "signal",
                result
            )

            # -------------------------------------------------
            # DECISION ENGINE
            # -------------------------------------------------

            pipeline_logger.info(
                f"[DECISION INPUT] "
                f"{symbol} "
                f"AI={result.action} "
                f"confidence={result.confidence:.4f}"
            )

            trade_signal = self.decision_engine.decide(
                result
            )

            # -------------------------------------------------
            # DECISION REJECTED
            # -------------------------------------------------

            if trade_signal is None:

                pipeline_logger.info(
                    f"[DECISION REJECTED] "
                    f"{symbol} "
                    f"AI={result.action} "
                    f"confidence={result.confidence:.4f}"
                )

                return

            # -------------------------------------------------
            # DECISION ACCEPTED
            # -------------------------------------------------

            pipeline_logger.success(
                f"[DECISION ACCEPTED] "
                f"{symbol} "
                f"{trade_signal.action} "
                f"confidence={trade_signal.confidence:.4f}"
            )

            # -------------------------------------------------
            # TRADE SIGNAL
            # -------------------------------------------------

            await self.bus.publish(
                "trade_signal",
                trade_signal
            )

            # -------------------------------------------------
            # PAPER TRADING
            # -------------------------------------------------

            await self.bus.publish(
                "paper_trade",
                trade_signal
            )

            logger.info(
                f"[PAPER READY] "
                f"{symbol} "
                f"{trade_signal.action}"
            )

        except Exception:

            logger.exception(
                "SignalProcessor failed."
            )

