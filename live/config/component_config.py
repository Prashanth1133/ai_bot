from __future__ import annotations

from dataclasses import dataclass, field


@dataclass(slots=True)
class ComponentConfig:

    name: str

    enabled: bool = True

    priority: int = 100

    dependencies: list[str] = field(
        default_factory=list
    )

    parameters: dict = field(
        default_factory=dict
    )