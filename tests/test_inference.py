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

        1,
        128,
        11

    )

    result = engine.predict(

        x

    )

    print(result)

    assert result is not None

    assert "signal" in result

    assert "confidence" in result

    assert "take_profit" in result

    assert "stop_loss" in result

    assert "market_regime" in result


if __name__ == "__main__":

    test_inference()