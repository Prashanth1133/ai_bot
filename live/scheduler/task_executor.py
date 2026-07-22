from __future__ import annotations

import inspect
import time


class TaskExecutor:

    async def execute(
        self,
        task,
    ):

        started = time.perf_counter()

        success = True

        try:

            result = task.coroutine()

            if inspect.isawaitable(result):
                await result

        except Exception:

            success = False

        runtime = (
            time.perf_counter()
            - started
        )

        return success, runtime