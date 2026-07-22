from ai.model import TradingTransformer
from ai.model_manager import ModelManager

model = TradingTransformer(

    input_dim=11

)

manager = ModelManager()

manager.register(

    "main",

    model

)

manager.load(

    "main",

    "models/main.pt"

)

print(

    manager.predict(

        "main",

        [[[0.0] * 11]]

    )

)