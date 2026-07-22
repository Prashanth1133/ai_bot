from __future__ import annotations

from dataclasses import dataclass, field

from live.config.config_source import ConfigSource


@dataclass(slots=True)
class ConfigEntry:

    key: str

    value: object

    source: ConfigSource = ConfigSource.DEFAULT

    description: str = ""

    readonly: bool = False

    metadata: dict = field(default_factory=dict)