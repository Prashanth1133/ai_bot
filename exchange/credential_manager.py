from __future__ import annotations

import os


class CredentialManager:

    @staticmethod
    def api_key():

        return os.getenv(
            "BINANCE_API_KEY",
            "",
        )

    @staticmethod
    def api_secret():

        return os.getenv(
            "BINANCE_API_SECRET",
            "",
        )