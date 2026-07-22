from ai.models.registry import (
    ModelRegistry
)

registry = ModelRegistry()

registry.load()


def infer(features):

    result = registry.predict(
        features
    )

    if result["buy"] > 0.80:
        return "BUY"

    if result["sell"] > 0.80:
        return "SELL"

    return "HOLD"