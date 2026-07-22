from __future__ import annotations

from portfolio.allocation import Allocation


class AllocationEngine:

    def allocate(

        self,

        capital: float,

        signals: list,

    ) -> list[Allocation]:

        if not signals:

            return []

        weight = 1.0 / len(signals)

        allocations = []

        for signal in signals:

            allocations.append(

                Allocation(

                    symbol=signal.symbol,

                    target_weight=weight,

                    capital=capital * weight,

                )

            )

        return allocations