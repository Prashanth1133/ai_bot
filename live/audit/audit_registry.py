from __future__ import annotations


class AuditRegistry:

    def __init__(self):

        self._records = {}

    def register(
        self,
        record,
    ):

        self._records[
            record.audit_id
        ] = record

    def get(
        self,
        audit_id: str,
    ):

        return self._records.get(audit_id)

    def remove(
        self,
        audit_id: str,
    ):

        self._records.pop(
            audit_id,
            None,
        )

    def all(self):

        return list(
            self._records.values()
        )

    def clear(self):

        self._records.clear()