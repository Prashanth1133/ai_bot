from production.production_manager import (
    ProductionManager
)


class ProductionInference:


    def __init__(self):

        self.manager = (

            ProductionManager()

        )


    def predict(

        self,
        data

    ):


        return (

            self.manager.evaluate(

                data

            )

        )