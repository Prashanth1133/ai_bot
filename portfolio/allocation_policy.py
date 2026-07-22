from __future__ import annotations

from dataclasses import dataclass


@dataclass(slots=True)
class AllocationPolicy:

    max_position_weight: float = 0.10

    min_position_weight: float = 0.01

    max_sector_weight: float = 0.30

    rebalance_threshold: float = 0.02

    allow_fractional: bool = True