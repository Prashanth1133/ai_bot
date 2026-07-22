class Ensemble:

    def predict(
        self,
        orderflow,
        transformer,
        news
    ):

        score = (
            orderflow * 0.5
            + transformer * 0.3
            + news * 0.2
        )

        return score