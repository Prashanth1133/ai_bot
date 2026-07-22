from __future__ import annotations

from dataclasses import dataclass, field


@dataclass(slots=True)
class AllocationResult:

    allocations: list = field(default_factory=list)

    remaining_cash: float = 0.0

    invested_cash: float = 0.0

    total_weight: float = 0.0

    metadata: dict = field(default_factory=dict)