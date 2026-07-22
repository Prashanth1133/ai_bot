import torch

from ai.inference import InferenceEngine


class LiveAIEngine:

    def __init__(

        self,
        model

    ):

        self.inference = (

            InferenceEngine(
                model
            )

        )

    def process(

        self,
        features

    ):

        if not isinstance(

            features,

            torch.Tensor

        ):

            features = torch.tensor(

                features,

                dtype=torch.float32

            )

        result = self.inference.predict(

            features

        )

        return {

            "signal":

                result["signal"],

            "confidence":

                round(

                    result["confidence"],

                    4

                ),

            "reversal":

                result["reversal"],

            "volatility":

                round(

                    result["volatility"],

                    4

                ),

            "take_profit":

                round(

                    result["take_profit"],

                    4

                ),

            "stop_loss":

                round(

                    result["stop_loss"],

                    4

                ),

            "market_regime":

                result["market_regime"]

        }