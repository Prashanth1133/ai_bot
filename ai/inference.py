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
        reversal_prob = 0.0

        if "reversal" in outputs:
            rev_tensor = outputs["reversal"]
            if rev_tensor.shape[-1] == 1:
                reversal_prob = float(torch.sigmoid(rev_tensor).squeeze().item())
                reversal = reversal_prob >= 0.5
            else:
                reversal_prediction = torch.argmax(rev_tensor, dim=-1)
                reversal = bool(reversal_prediction[0].item())

        market_regime = 0
        if "market_regime" in outputs:
            market_regime = int(
                torch.argmax(
                    outputs["market_regime"],
                    dim=-1,
                )[0].item()
            )

        # Multi-horizon and risk scalars
        ret_15m = scalar_output("return_15m", 0.0)
        ret_1h = scalar_output("return_1h", 0.0)
        ret_4h = scalar_output("return_4h", 0.0)
        max_ret_1h = scalar_output("max_return_1h", 0.0)
        min_ret_1h = scalar_output("min_return_1h", 0.0)
        tp = scalar_output("take_profit", 0.0)
        sl = scalar_output("stop_loss", 0.0)
        vol = scalar_output("volatility", 0.0)

        # ======================================================
        # LOG
        # ======================================================

        ai_logger.info(
            "[AI PREDICTION] "
            f"Prediction={signal} "
            f"Confidence={confidence_value:.4f} "
            f"SELL={probability_sell:.4f} "
            f"HOLD={probability_hold:.4f} "
            f"BUY={probability_buy:.4f} "
            f"TP={tp:.4f} SL={sl:.4f}"
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
            "reversal_probability": reversal_prob,
            "return_15m": ret_15m,
            "return_1h": ret_1h,
            "return_4h": ret_4h,
            "max_return_1h": max_ret_1h,
            "min_return_1h": min_ret_1h,
            "volatility": vol,
            "take_profit": tp,
            "stop_loss": sl,
            "market_regime": market_regime,
        }
