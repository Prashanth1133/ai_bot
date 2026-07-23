class ProductionSignal:


    def generate(

        self,
        signal,
        confidence

    ):


        if confidence < 0.70:

            return "NO TRADE"


        return signal