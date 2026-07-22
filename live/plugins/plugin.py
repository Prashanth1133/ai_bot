from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime

from live.plugins.plugin_state import PluginState


@dataclass(slots=True)
class Plugin:

    name: str

    version: str = "1.0.0"

    author: str = ""

    description: str = ""

    state: PluginState = PluginState.REGISTERED

    enabled: bool = True

    metadata: dict = field(default_factory=dict)

    loaded_at: datetime | None = None