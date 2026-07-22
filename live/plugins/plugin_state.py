from enum import Enum


class PluginState(Enum):

    REGISTERED = "REGISTERED"

    LOADED = "LOADED"

    INITIALIZED = "INITIALIZED"

    RUNNING = "RUNNING"

    DISABLED = "DISABLED"

    FAILED = "FAILED"

    UNLOADED = "UNLOADED"