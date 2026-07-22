class SessionRegistry:

    def __init__(self):

        self._sessions = {}

    def register(self, session):

        self._sessions[
            session.session_id
        ] = session

    def get(self, session_id):

        return self._sessions.get(session_id)

    def remove(self, session_id):

        self._sessions.pop(session_id, None)

    def all(self):

        return list(self._sessions.values())

    def clear(self):

        self._sessions.clear()