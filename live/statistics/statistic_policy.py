from dataclasses import dataclass


@dataclass(slots=True)
class StatisticPolicy:

    enabled: bool = True

    retention: int = 10000

    auto_cleanup: bool = True

    export_interval: int = 300