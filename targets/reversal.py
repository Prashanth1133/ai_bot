class ReversalTarget:

    def generate(

        self,

        candles,

        index,

        lookahead=30,

        threshold=0.02

    ):

        entry = candles[index].close

        future = candles[index+1:index+lookahead]

        high = max(x.high for x in future)

        low = min(x.low for x in future)

        if (high-entry)/entry > threshold:

            return 1

        if (entry-low)/entry > threshold:

            return -1

        return 0