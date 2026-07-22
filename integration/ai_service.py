from ai.live_ai_engine import LiveAIEngine
from integration.model_loader import ModelLoader


class AIService:

    def __init__(self):

        loader = ModelLoader()

        model = loader.load()

        self.engine = (

            LiveAIEngine(

                model

            )

        )

    def predict(

        self,
        features

    ):

        return self.engine.process(

            features

        )