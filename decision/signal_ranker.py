class SignalRanker:

    def rank(

        self,

        signals,

    ):

        return sorted(

            signals,

            key=lambda x: x.confidence,

            reverse=True,

        )