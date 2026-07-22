from __future__ import annotations


class DiagnosticRegistry:

    def __init__(self):

        self._checks = {}

    def register(
        self,
        name: str,
        check,
    ):

        self._checks[name] = check

    def get(
        self,
        name: str,
    ):

        return self._checks.get(name)

    def checks(self):

        return dict(self._checks)

    def remove(
        self,
        name: str,
    ):

        self._checks.pop(name, None)

    def clear(self):

        self._checks.clear()