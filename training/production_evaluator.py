class ProductionEvaluator:


    def evaluate(

        self,
        metrics

    ):


        print("\n")


        print(

            "="*60

        )


        print(

            "PRODUCTION REPORT"

        )


        print(

            "="*60

        )


        for key,value in (

            metrics.items()

        ):


            print(

                key,

                ":",

                value

            )


        print(

            "="*60

        )


        return metrics