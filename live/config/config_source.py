from enum import Enum


class ConfigSource(Enum):

    FILE = "FILE"

    ENVIRONMENT = "ENVIRONMENT"

    REMOTE = "REMOTE"

    MEMORY = "MEMORY"

    DEFAULT = "DEFAULT"