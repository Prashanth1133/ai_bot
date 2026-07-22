class ConfidenceEngine:

    """
    Calculates the final confidence score
    using weighted probabilities.
    """

    def calculate(

        self,

        signal,

    ):

        confidence = 0.0

        confidence += signal.ai_probability * 0.40

        confidence += signal.smart_money_score * 0.25

        confidence += signal.orderflow_score * 0.20

        confidence += signal.news_score * 0.15

        return min(confidence, 1.0)