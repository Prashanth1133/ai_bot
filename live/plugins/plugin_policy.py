from dataclasses import dataclass


@dataclass(slots=True)
class PluginPolicy:

    auto_load: bool = True

    allow_hot_reload: bool = True

    verify_dependencies: bool = True