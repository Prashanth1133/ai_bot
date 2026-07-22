import torch


class ConfidenceEngine:

    @staticmethod
    def score(logits):

        probabilities = torch.softmax(
            logits,
            dim=1
        )

        confidence, prediction = torch.max(
            probabilities,
            dim=1
        )

        return (
            prediction.item(),
            confidence.item()
        )