from enum import Enum


class RecoveryState(Enum):

    IDLE = "IDLE"

    RECOVERING = "RECOVERING"

    COMPLETED = "COMPLETED"

    FAILED = "FAILED"