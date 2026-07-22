import torch
import numpy as np


class InferenceEngine:

    def __init__(self, model):

        self.model = model

        self.model.eval()

    @torch.no_grad()
    def predict(self, features):

        # ------------------------
        # Convert input to tensor
        # ------------------------

        if isinstance(features, list):

            features = torch.tensor(

                features,

                dtype=torch.float32

            )

        elif isinstance(features, np.ndarray):

            features = torch.from_numpy(

                features

            ).float()

        # ------------------------
        # Add batch dimension
        # ------------------------

        if len(features.shape) == 2:

            features = features.unsqueeze(

                0

            )

        outputs = self.model(

            features

        )

        direction = torch.argmax(

            outputs["direction"],

            dim=-1

        ).item()

        reversal = torch.argmax(

            outputs["reversal"],

            dim=-1

        ).item()

        confidence = float(

            outputs["confidence"]

            .squeeze()

            .item()

        )

        signal_map = {

            0: "SELL",
            1: "HOLD",
            2: "BUY"

        }

        return {

            "signal":

                signal_map[

                    direction

                ],

            "confidence":

                confidence,

            "reversal":

                bool(

                    reversal

                ),

            "volatility":

                float(

                    outputs["volatility"]

                    .squeeze()

                    .item()

                ),

            "take_profit":

                float(

                    outputs["take_profit"]

                    .squeeze()

                    .item()

                ),

            "stop_loss":

                float(

                    outputs["stop_loss"]

                    .squeeze()

                    .item()

                ),

            "market_regime":

                int(

                    torch.argmax(

                        outputs["market_regime"],

                        dim=-1

                    ).item()

                )

        }