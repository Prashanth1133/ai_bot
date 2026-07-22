from __future__ import annotations

import inspect
from typing import Any, Dict, Optional

from execution.execution_mode import ExecutionMode


class OrderRouter:
    """
    Routes execution requests to the appropriate execution engine.

    Supports:
    - Paper execution
    - Live execution
    - Sync/async execution engines
    """

    def __init__(self) -> None:
        self._engines: Dict[ExecutionMode, Any] = {}

    def register(self, mode: ExecutionMode, engine: Any) -> None:
        self._engines[mode] = engine

    def register_paper(self, engine: Any) -> None:
        self.register(ExecutionMode.PAPER, engine)

    def register_live(self, engine: Any) -> None:
        self.register(ExecutionMode.LIVE, engine)

    def unregister(self, mode: ExecutionMode) -> None:
        self._engines.pop(mode, None)

    def get_engine(self, mode: ExecutionMode) -> Optional[Any]:
        return self._engines.get(mode)

    async def execute(
        self,
        mode: ExecutionMode,
        trade: Any,
        risk: Any = None,
        **kwargs,
    ) -> Any:
        engine = self.get_engine(mode)

        if engine is None:
            raise RuntimeError(
                f"No execution engine registered for {mode!s}"
            )

        if not hasattr(engine, "execute"):
            raise AttributeError(
                f"{engine.__class__.__name__} has no execute() method."
            )

        result = engine.execute(
            trade=trade,
            risk=risk,
            **kwargs,
        )

        if inspect.isawaitable(result):
            result = await result

        return result