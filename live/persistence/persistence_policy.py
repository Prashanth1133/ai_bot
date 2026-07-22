from dataclasses import dataclass


@dataclass(slots=True)
class PersistencePolicy:

    enabled: bool = True

    autosave_interval: int = 60

    compression: bool = False

    backup_before_save: bool = True