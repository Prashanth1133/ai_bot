import torch

from ai.model import TradingTransformer
from ai.inference import InferenceEngine


def test_inference():

    model = TradingTransformer(

        input_dim=11

    )

    engine = InferenceEngine(

        model

    )

    x = torch.randn(

        1,      # batch
        128,    # sequence length
        11      # features
    )

    prediction = engine.predict(

        x

    )

    assert prediction is not None

    assert "signal" in prediction

    assert "confidence" in prediction

    assert "take_profit" in prediction

    assert "stop_loss" in prediction

    assert "market_regime" in prediction


if __name__ == "__main__":

    test_inference()

    print(

        "AI inference test passed."

    )