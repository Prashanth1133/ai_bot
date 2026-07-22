from __future__ import annotations

import hashlib
import hmac


class RequestSigner:

    def __init__(
        self,
        secret: str,
    ):
        self.secret = secret.encode()

    def sign(
        self,
        query: str,
    ):

        return hmac.new(
            self.secret,
            query.encode(),
            hashlib.sha256,
        ).hexdigest()