from __future__ import annotations

import numpy as np
from app.logger import logger
from logs.log_manager import ai_logger, pipeline_logger
from decision.decision_engine import DecisionEngine
from live.signal_engine import LiveSignalEngine


class SignalProcessor:

    def __init__(self, bus):
        self.bus = bus
        self.engine = LiveSignalEngine()
        self.decision_engine = DecisionEngine()
        self.signal_engine = None

    def set_engine(self, engine):
        self.signal_engine = engine

    async def on_features(self, sequence_packet):
        try:
            engine = self.signal_engine or self.engine
            symbol = sequence_packet["symbol"]
            sequence = sequence_packet["values"]

            seq_arr = np.asarray(sequence)
            seq_len = seq_arr.shape[1] if seq_arr.ndim == 3 else (seq_arr.shape[0] if seq_arr.ndim == 2 else len(sequence))
            feat_count = seq_arr.shape[2] if seq_arr.ndim == 3 else (seq_arr.shape[1] if seq_arr.ndim == 2 else 0)

            # -------------------------------------------------
            # AI INPUT LOGGING (Accurate Tensor Dimension Reporting)
            # -------------------------------------------------
            ai_logger.info(
                f"[AI INPUT] "
                f"{symbol} "
                f"shape={seq_arr.shape} "
                f"sequence_length={seq_len} "
                f"features={feat_count}"
            )

            # -------------------------------------------------
            # REAL AI INFERENCE
            # -------------------------------------------------
            result = engine.evaluate(
                sequence,
                symbol=symbol,
            )

            if result is None:
                ai_logger.info(
                    f"[AI RESULT] "
                    f"{symbol} "
                    f"FILTERED"
                )
                return

            ai_logger.success(
                f"[AI FIRED] "
                f"{symbol} "
                f"ACTION={result.action} "
                f"CONFIDENCE={result.confidence:.4f}"
            )

            await self.bus.publish("signal", result)

            pipeline_logger.info(
                f"[DECISION INPUT] "
                f"{symbol} "
                f"AI={result.action} "
                f"confidence={result.confidence:.4f}"
            )

            trade_signal = self.decision_engine.decide(result)

            if trade_signal is None:
                pipeline_logger.info(
                    f"[DECISION REJECTED] "
                    f"{symbol} "
                    f"AI={result.action} "
                    f"confidence={trade_signal.confidence if trade_signal else 0.0:.4f}"
                )
                return

            pipeline_logger.success(
                f"[DECISION ACCEPTED] "
                f"{symbol} "
                f"{trade_signal.action} "
                f"confidence={trade_signal.confidence:.4f}"
            )

            await self.bus.publish("trade_signal", trade_signal)
            await self.bus.publish("paper_trade", trade_signal)

            logger.info(f"[PAPER READY] {symbol} {trade_signal.action}")

        except Exception:
            logger.exception("SignalProcessor failed.")
