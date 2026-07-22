from __future__ import annotations

import asyncio

from live.diagnostics.diagnostic_result import (
    DiagnosticResult,
)


class DiagnosticManager:

    def __init__(self):

        self.registry = None

        self.history = None

    def attach_registry(
        self,
        registry,
    ):

        self.registry = registry

    def attach_history(
        self,
        history,
    ):

        self.history = history

    async def run(self):

        results = []

        for name, check in (

            self.registry.checks().items()

        ):

            output = check()

            if asyncio.iscoroutine(output):

                output = await output

            if isinstance(output, tuple):

                passed, message = output

            else:

                passed = bool(output)

                message = ""

            result = DiagnosticResult(

                component=name,

                passed=passed,

                message=message,

            )

            if self.history:

                self.history.add(result)

            results.append(result)

        return results