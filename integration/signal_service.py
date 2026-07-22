class SignalService:

    def __init__(self):

        self.history = []

    def publish(

        self,
        signal

    ):

        self.history.append(

            signal

        )

        print(

            f"[AI] "
            f"{signal['signal']} "
            f"({signal['confidence']:.2%})"
        )

    def last(self):

        if not self.history:

            return None

        return self.history[-1]

    def total(self):

        return len(

            self.history

        )