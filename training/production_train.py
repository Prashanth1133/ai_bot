import os

from ai.model import TradingTransformer
from ai.trainer import Trainer

from training.production_dataset import ProductionDataset
from training.production_checkpoint import ProductionCheckpoint


class ProductionTrain:

    def train(

        self,
        path,
        save_path,
        drive_path,
        epochs=100

    ):

        print("\nLoading Dataset ...")

        X, y, dataset = (

            ProductionDataset()

            .load(

                path

            )

        )

        print("Dataset Size :", len(X))

        #################################################

        # Create model

        model = TradingTransformer(

            input_dim=X.shape[-1]

        )

        #################################################

        # Create Google Drive folder if it does not exist

        os.makedirs(drive_path, exist_ok=True)

        #################################################

        # Trainer

        trainer = Trainer(

            model=model,

            dataset=dataset,

            save_path=save_path,

            drive_path=drive_path,

            resume=True

        )

        #################################################

        trainer.train(

            epochs=epochs

        )

        #################################################

        # Export final model

        ProductionCheckpoint().save(

            model,

            save_path

        )

        print("\nProduction Model Saved.")

        return model