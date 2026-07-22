class SignalQuality:

    def score(

        self,

        signal,

    ):

        score = 0.0

        score += signal.confidence

        score += signal.smart_money_score

        score += signal.orderflow_score

        return score / 3