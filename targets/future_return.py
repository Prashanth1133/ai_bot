class FutureReturnTarget:

    def generate(

        self,

        candles,

        index,

        horizon=20

    ):

        entry = candles[index].close

        future = candles[index+horizon].close

        return (future-entry)/entry