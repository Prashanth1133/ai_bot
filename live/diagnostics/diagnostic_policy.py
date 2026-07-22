from dataclasses import dataclass


@dataclass(slots=True)
class DiagnosticPolicy:

    enabled: bool = True

    interval: float = 60.0

    stop_on_failure: bool = False

    save_history: bool = True