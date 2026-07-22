import torch

from live.live_ai_engine import (
    LiveAIEngine
)

x = torch.randn(

    128,
    11

)

engine = LiveAIEngine(

    "models/btc_v1.pt"

)

print(

    engine.predict(

        x

    )

)