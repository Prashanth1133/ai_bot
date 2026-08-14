import torch
from pathlib import Path

from ai.model import TradingTransformer
from ai.inference import InferenceEngine


class LiveAIEngine:

    def __init__(

        self,
        model_path,
        input_dim=11

    ):

        if Path(model_path).is_file():
            self.model = TradingTransformer(input_dim=input_dim)
            self.model.load_state_dict(torch.load(model_path, map_location="cpu", weights_only=True))
        else:
            from ai.models.model_manager import ModelManager
            self.model = ModelManager().load_latest()

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
