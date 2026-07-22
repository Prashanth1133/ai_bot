from ai.model import TradingTransformer
from ai.model_manager import ModelManager


class ModelLoader:

    def __init__(

        self,
        input_dim=11

    ):

        self.model = (

            TradingTransformer(

                input_dim=input_dim

            )

        )

        self.manager = (

            ModelManager()

        )

        self.manager.register(

            "main",

            self.model

        )

    def load(self):

        self.manager.load(

            "main",

            "models/main.pt"

        )

        return self.model