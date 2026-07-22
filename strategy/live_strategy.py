from __future__ import annotations

import inspect

from strategy.strategy_result import StrategyResult


class LiveStrategy:

    async def evaluate(
        self,
        context,
    ) -> StrategyResult:

        prediction = self.predict(context)

        if inspect.isawaitable(prediction):
            prediction = await prediction

        return prediction

    def predict(
        self,
        context,
    ):

        raise NotImplementedError