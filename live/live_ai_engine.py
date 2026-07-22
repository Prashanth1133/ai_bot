import torch

from ai.model import TradingTransformer
from ai.inference import InferenceEngine


class LiveAIEngine:

    def __init__(

        self,
        model_path,
        input_dim=11

    ):

        self.model = TradingTransformer(

            input_dim=input_dim

        )

        self.model.load_state_dict(

            torch.load(

                model_path,

                map_location="cpu"

            )

        )

        self.engine = InferenceEngine(

            self.model

        )

    def predict(

        self,
        features

    ):

        return self.engine.predict(

            features

        )