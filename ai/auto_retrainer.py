import os


class AutoRetrainer:

    def should_retrain(
        self,
        accuracy
    ):

        return accuracy < 70

    def retrain(self):

        os.system(
            "python -m "
            "ai.trainer.train_xgboost"
        )