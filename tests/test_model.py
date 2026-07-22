import torch

from ai.model import TradingTransformer

model = TradingTransformer(
    input_dim=11
)

x = torch.randn(
    8,
    128,
    11
)

outputs = model(x)

for key in outputs:

    print(
        key,
        outputs[key].shape
        if hasattr(
            outputs[key],
            "shape"
        )
        else len(outputs[key])
    )