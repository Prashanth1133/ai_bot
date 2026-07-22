from __future__ import annotations

import inspect


class DecisionPipeline:

    def __init__(
        self,
        strategy_manager,
        ai_engine,
        risk_manager,
        decision_engine,
    ):
        self.strategy_manager = strategy_manager
        self.ai_engine = ai_engine
        self.risk_manager = risk_manager
        self.decision_engine = decision_engine

    async def run(
        self,
        context,
    ):

        strategy = self.strategy_manager.run(context)

        if inspect.isawaitable(strategy):
            strategy = await strategy

        ai_prediction = self.ai_engine.predict(
            context,
        )

        if inspect.isawaitable(ai_prediction):
            ai_prediction = await ai_prediction

        risk = self.risk_manager.evaluate(
            strategy,
            ai_prediction,
        )

        if inspect.isawaitable(risk):
            risk = await risk

        decision = self.decision_engine.evaluate(
            strategy,
            ai_prediction,
            risk,
        )

        if inspect.isawaitable(decision):
            decision = await decision

        return decision