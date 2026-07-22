class FutureAnalyzer:

    """
    Computes future market statistics
    over a look-ahead window.
    """

    def analyze(

        self,

        candles,

        index,

        window=40

    ):

        current = candles[index].close

        future = candles[
            index+1:index+window+1
        ]

        if not future:

            return None

        highest = max(

            c.high

            for c in future

        )

        lowest = min(

            c.low

            for c in future

        )

        return {

            "entry": current,

            "highest": highest,

            "lowest": lowest

        }