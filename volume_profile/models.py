from __future__ import annotations

from dataclasses import dataclass
from decimal import Decimal


@dataclass(slots=True)
class VolumeProfile:

    poc: Decimal

    vah: Decimal

    val: Decimal

    hvn: list

    lvn: list

    total_volume: Decimal