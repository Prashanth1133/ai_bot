from enum import Enum


class ServiceState(Enum):

    CREATED = "CREATED"

    STARTING = "STARTING"

    RUNNING = "RUNNING"

    STOPPING = "STOPPING"

    STOPPED = "STOPPED"

    FAILED = "FAILED"