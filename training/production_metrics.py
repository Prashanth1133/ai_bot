class ProductionMetrics:


    def calculate(

        self,
        accuracy,
        loss

    ):


        return {

            "accuracy":

            round(

                accuracy,

                4

            ),

            "loss":

            round(

                loss,

                4

            )

        }