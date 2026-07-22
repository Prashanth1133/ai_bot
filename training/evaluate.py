import torch

from ai.model import TradingTransformer
from ai.inference import InferenceEngine


model = TradingTransformer(

    input_dim=11

)

model.load_state_dict(

    torch.load(

        "models/btc_v1.pt",

        map_location="cpu"

    )

)

engine = InferenceEngine(

    model

)

x = torch.randn(

    128,
    11

)

print(

    engine.predict(

        x

    )

)