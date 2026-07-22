from collections import Counter


class EnsembleEngine:

    @staticmethod
    def vote(predictions):

        result = Counter(
            predictions
        )

        return result.most_common(
            1
        )[0][0]