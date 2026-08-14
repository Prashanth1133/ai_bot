from __future__ import annotations

import numpy as np

from app.settings import settings
from ai.inference import InferenceEngine
from ai.models.model_manager import ModelManager
from models.signal import Signal


class LiveSignalEngine:

    MARKET_REGIME_MAP = {
        0: "RANGING",
        1: "TREND",
        2: "VOLATILE",
    }

    def __init__(
        self,
        model=None,
        confidence_threshold=None,
    ):

        self.model = (
            model
            or ModelManager().load_latest()
        )

        self.predictor = InferenceEngine(
            self.model
        )

        self.threshold = (
            settings.CONFIDENCE_THRESHOLD
            if confidence_threshold is None
            else confidence_threshold
        )

    # =====================================================
    # Evaluate
    # =====================================================

    def evaluate(
        self,
        sequence,
        *,
        symbol="BTCUSDT",
    ):

        # -------------------------------------------------
        # Convert
        # -------------------------------------------------

        sequence = np.asarray(
            sequence,
            dtype=np.float32,
        )

        # -------------------------------------------------
        # Validate shape
        # -------------------------------------------------

        if sequence.ndim == 2:

            sequence = np.expand_dims(
                sequence,
                axis=0,
            )

        if sequence.ndim != 3:

            raise ValueError(
                f"Expected [batch, sequence, features], "
                f"got {sequence.shape}"
            )

        if sequence.shape[-1] != settings.MODEL_INPUT_DIM:

            raise ValueError(
                f"Expected "
                f"{settings.MODEL_INPUT_DIM} features, "
                f"got {sequence.shape[-1]}"
            )

        # -------------------------------------------------
        # Prediction
        # -------------------------------------------------

        from logs.log_manager import ai_logger

        ai_logger.info(
            f"[AI INFERENCE START] "
            f"{symbol} "
            f"shape={sequence.shape}"
        )

        result = self.predictor.predict(
            sequence
        )

        ai_logger.info(
            f"[AI INFERENCE RAW] "
            f"{symbol} "
            f"result={result}"
        )

        action = result["signal"]

        confidence = float(
            result["confidence"]
        )

        # -------------------------------------------------
        # Log every prediction
        # -------------------------------------------------

        ai_logger.info(
            f"[LIVE AI] "
            f"{symbol} "
            f"{action} "
            f"confidence={confidence:.4f}"
        )

        # -------------------------------------------------
        # Confidence filter
        # -------------------------------------------------

        if confidence < self.threshold:

            ai_logger.info(
                f"[AI FILTER] "
                f"{symbol} "
                f"{action} "
                f"confidence={confidence:.4f} "
                f"< threshold={self.threshold:.4f}"
            )

            return None

        # -------------------------------------------------
        # HOLD filter
        # -------------------------------------------------

        if action == "HOLD":

            ai_logger.info(
                f"[AI FILTER] "
                f"{symbol} HOLD"
            )

            return None

        # -------------------------------------------------
        # Latest candle close
        #
        # sequence shape: [batch, sequence, features]
        # feature 3 = close
        # -------------------------------------------------

        entry = float(
            sequence[0, -1, 3]
        )

        # -------------------------------------------------
        # TP / SL
        # -------------------------------------------------

        tp_distance = max(
            float(result.get("take_profit", 0.0)),
            0.0,
        )

        sl_distance = max(
            float(result.get("stop_loss", 0.0)),
            0.0,
        )

        if action == "BUY":

            take_profit = entry * (
                1.0 + tp_distance
            )

            stop_loss = entry * (
                1.0 - sl_distance
            )

        else:

            take_profit = entry * (
                1.0 - tp_distance
            )

            stop_loss = entry * (
                1.0 + sl_distance
            )

        # -------------------------------------------------
        # Validate levels
        # -------------------------------------------------

        if action == "BUY":

            valid_levels = (
                take_profit > entry > stop_loss
            )

        else:

            valid_levels = (
                take_profit < entry < stop_loss
            )

        if not valid_levels:

            ai_logger.warning(
                f"[AI INVALID LEVELS] "
                f"{symbol} "
                f"action={action} "
                f"entry={entry} "
                f"TP={take_profit} "
                f"SL={stop_loss}"
            )

            return None

        # -------------------------------------------------
        # Market regime
        # -------------------------------------------------

        regime_id = int(
            result.get(
                "market_regime",
                0,
            )
        )

        market_regime = (
            self.MARKET_REGIME_MAP.get(
                regime_id,
                "UNKNOWN",
            )
        )

        # -------------------------------------------------
        # Final signal
        # -------------------------------------------------

        return Signal(
            symbol=symbol,
            action=action,
            side=action,
            confidence=confidence,
            entry_price=entry,
            take_profit=take_profit,
            stop_loss=stop_loss,
            reversal=bool(
                result.get(
                    "reversal",
                    False,
                )
            ),
            market_regime=market_regime,
            features={
                "volatility": float(
                    result.get(
                        "volatility",
                        0.0,
                    )
                )
            },
        )
