from transformers import (
    pipeline
)

classifier = pipeline(
    "text-classification",
    model="ProsusAI/finbert"
)


class NewsSentiment:

    def analyze(
        self,
        text
    ):

        result = classifier(
            text
        )[0]

        return {
            "label":
            result["label"],

            "score":
            result["score"]
        }