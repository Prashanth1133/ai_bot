# ai/predictor.py

from ai.models.model_manager import ModelManager
from ai.models.inference_engine import InferenceEngine


class Predictor:


    def __init__(self):

        self.manager = ModelManager()

        self.model = self.manager.load_latest()

        self.engine = InferenceEngine()



    def predict(

        self,

        features

    ):

        result = self.engine.predict(

            features

        )

        return result