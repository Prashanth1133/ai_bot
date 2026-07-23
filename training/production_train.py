from ai.model import (
    TradingTransformer
)

from ai.trainer import (
    Trainer
)

from training.production_dataset import (
    ProductionDataset
)

from training.production_checkpoint import (
    ProductionCheckpoint
)


class ProductionTrain:


    def train(

        self,
        path,
        save_path,
        epochs=100

    ):


        print(

            "\nLoading Dataset ..."

        )


        X, y, dataset = (

            ProductionDataset()

            .load(

                path

            )

        )


        print(

            "Dataset Size :",

            len(X)

        )


        #################################################


        model = (

            TradingTransformer(

                input_dim=X.shape[-1]

            )

        )


        #################################################


        trainer = (

            Trainer(

                model=model,
                dataset=dataset

            )

        )


        #################################################


        trainer.train(

            epochs=epochs

        )


        #################################################


        ProductionCheckpoint().save(

            model,

            save_path

        )


        print(

            "\nProduction Model Saved."

        )


        return model