class ModelSelector:

    def best(

        self,

        results,

    ):

        return max(

            results,

            key=lambda x: x["accuracy"]

        )