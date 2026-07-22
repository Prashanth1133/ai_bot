from __future__ import annotations

import uuid


class ClientOrderIdGenerator:

    @staticmethod
    def generate():

        return uuid.uuid4().hex