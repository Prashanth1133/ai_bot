class ProductionReport:


    def generate(

        self,
        result

    ):


        print("\n")

        print("=" * 60)

        print(

            "PRODUCTION V1 REPORT"

        )

        print("=" * 60)

        print(

            f"Accuracy : "

            f"{result['accuracy']:.4f}"

        )


        print(

            f"Mean Error : "

            f"{result['mean_error']:.6f}"

        )


        print(

            f"Confidence : "

            f"{result['confidence']:.4f}"

        )


        print("=" * 60)

        print("\n")