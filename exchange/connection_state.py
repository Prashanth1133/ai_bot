from __future__ import annotations

from enum import Enum


class ConnectionState(Enum):

    DISCONNECTED = "DISCONNECTED"

    CONNECTING = "CONNECTING"

    CONNECTED = "CONNECTED"

    RECONNECTING = "RECONNECTING"

    CLOSED = "CLOSED"