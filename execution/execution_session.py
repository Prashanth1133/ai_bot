from __future__ import annotations

from uuid import uuid4
from datetime import datetime


class ExecutionSession:

    def __init__(self):

        self.session_id = str(uuid4())

        self.started = datetime.utcnow()

    def as_dict(self):

        return {
            "session_id": self.session_id,
            "started": self.started.isoformat(),
        }