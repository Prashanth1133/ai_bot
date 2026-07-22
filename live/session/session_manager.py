from datetime import datetime

from live.session.session_state import (
    SessionState,
)


class SessionManager:

    def __init__(

        self,

        registry,

        history=None,

    ):

        self.registry = registry

        self.history = history

    def connect(self, session):

        session.state = (
            SessionState.CONNECTED
        )

        session.connected_at = (
            datetime.utcnow()
        )

        if self.history:

            self.history.add(session)

    def disconnect(self, session):

        session.state = (
            SessionState.DISCONNECTED
        )

        session.disconnected_at = (
            datetime.utcnow()
        )

        if self.history:

            self.history.add(session)