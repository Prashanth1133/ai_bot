import torch

from ai.model import TradingTransformer


model = TradingTransformer(

    input_dim=11

)

x = torch.randn(

    2,
    64,
    11

)

outputs = model(

    x

)

print(

    outputs.keys()

)