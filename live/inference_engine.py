from __future__ import annotations

import torch


class LiveInferenceEngine:

    def __init__(self, model):

        self.model = model

        self.model.eval()

    ############################################################

    @torch.no_grad()
    def predict(self, feature_vector):

        x = torch.tensor(
            feature_vector,
            dtype=torch.float32,
        ).unsqueeze(0)

        output = self.model(x)

        if isinstance(output, tuple):
            output = output[0]

        probabilities = torch.softmax(
            output,
            dim=1,
        )

        confidence, prediction = torch.max(
            probabilities,
            dim=1,
        )

        return {
            "prediction": int(prediction.item()),
            "confidence": float(confidence.item()),
            "probabilities": probabilities.squeeze().tolist(),
        }