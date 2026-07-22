from __future__ import annotations

import inspect


class StrategyManager:

    def __init__(
        self,
        selector,
        signal_filter,
    ):

        self.selector = selector

        self.signal_filter = signal_filter

    async def run(
        self,
        regime: str,
        context,
    ):

        strategy = self.selector.select(regime)

        if strategy is None:
            return None

        result = strategy.evaluate(context)

        if inspect.isawaitable(result):
            result = await result

        if not self.signal_filter.allow(result):
            return None

        return result