from __future__ import annotations


class StrategySelector:

    def __init__(
        self,
        registry,
    ):
        self.registry = registry

    def select(
        self,
        regime: str,
    ):

        strategy = self.registry.get(regime)

        if strategy is not None:
            return strategy

        return self.registry.get("default")