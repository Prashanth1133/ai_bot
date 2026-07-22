import torch

from ai.model import TradingModel
from ai.confidence import ConfidenceEngine


class Predictor:

    def __init__(
        self,
        model_path,
        input_size
    ):

        self.model = TradingModel(
            input_size
        )

        self.model.load_state_dict(
            torch.load(model_path)
        )

        self.model.eval()

    def predict(self, features):

        tensor = torch.tensor(
            features
        ).float().unsqueeze(0)

        with torch.no_grad():

            logits = self.model(
                tensor
            )

        return ConfidenceEngine.score(
            logits
        )