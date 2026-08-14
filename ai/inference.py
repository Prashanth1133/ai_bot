from __future__ import annotations

import numpy as np
import torch

from logs.log_manager import ai_logger


class InferenceEngine:

    SIGNAL_MAP = {
        0: "SELL",
        1: "HOLD",
        2: "BUY",
    }

    def __init__(self, model):

        self.model = model
        self.model.eval()

    @torch.no_grad()
    def predict(self, features):

        # ======================================================
        # INPUT
        # ======================================================

        if isinstance(features, list):

            features = torch.tensor(
                features,
                dtype=torch.float32,
            )

        elif isinstance(features, np.ndarray):

            features = torch.from_numpy(
                features
            ).float()

        elif not isinstance(features, torch.Tensor):

            raise TypeError(
                "Inference input must be list, numpy array "
                "or torch.Tensor."
            )

        # ======================================================
        # SHAPE
        # ======================================================

        if features.ndim == 2:

            # [sequence, features]
            features = features.unsqueeze(0)

        elif features.ndim != 3:

            raise ValueError(
                "Expected [sequence, features] or "
                "[batch, sequence, features]. "
                f"Got {tuple(features.shape)}"
            )

        # ======================================================
        # MODEL DEVICE
        # ======================================================

        device = next(
            self.model.parameters()
        ).device

        features = features.to(device)

        # ======================================================
        # MODEL
        # ======================================================

        outputs = self.model(
            features
        )

        # ======================================================
        # SIGNAL LOGITS
        # ======================================================

        logits = outputs.get("signal_logits")
        if logits is None:
            logits = outputs.get("direction")

        if logits is None:

            raise RuntimeError(
                "Production model output does not contain "
                "'signal_logits' or 'direction'. "
                f"Available outputs: {list(outputs.keys())}"
            )

        probabilities = torch.softmax(
            logits,
            dim=-1,
        )

        confidence, prediction = torch.max(
            probabilities,
            dim=-1,
        )

        direction = int(
            prediction[0].item()
        )

        signal = self.SIGNAL_MAP.get(
            direction,
            "HOLD",
        )

        confidence_value = float(
            confidence[0].item()
        )

        # ======================================================
        # PROBABILITIES
        # ======================================================

        probability_sell = float(
            probabilities[0, 0].item()
        )

        probability_hold = float(
            probabilities[0, 1].item()
        )

        probability_buy = float(
            probabilities[0, 2].item()
        )

        # ======================================================
        # AUXILIARY HEADS
        # ======================================================

        def scalar_output(name, default=0.0):

            value = outputs.get(name)

            if value is None:
                return default

            return float(
                value.squeeze().item()
            )

        reversal = False

        if "reversal" in outputs:

            reversal_prediction = torch.argmax(
                outputs["reversal"],
                dim=-1,
            )

            reversal = bool(
                reversal_prediction[0].item()
            )

        market_regime = 0

        if "market_regime" in outputs:

            market_regime = int(
                torch.argmax(
                    outputs["market_regime"],
                    dim=-1,
                )[0].item()
            )

        # ======================================================
        # LOG
        # ======================================================

        ai_logger.info(
            "[AI PREDICTION] "
            f"Prediction={signal} "
            f"Confidence={confidence_value:.4f} "
            f"SELL={probability_sell:.4f} "
            f"HOLD={probability_hold:.4f} "
            f"BUY={probability_buy:.4f}"
        )

        # ======================================================
        # RESULT
        # ======================================================

        return {

            "signal": signal,

            "confidence": confidence_value,

            "probability_sell": probability_sell,

            "probability_hold": probability_hold,

            "probability_buy": probability_buy,

            "reversal": reversal,

            "volatility": scalar_output(
                "volatility"
            ),

            "take_profit": scalar_output(
                "take_profit"
            ),

            "stop_loss": scalar_output(
                "stop_loss"
            ),

            "market_regime": market_regime,
        }
