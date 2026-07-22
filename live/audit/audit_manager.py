from __future__ import annotations

from live.audit.audit_record import AuditRecord


class AuditManager:

    def __init__(self):

        self.registry = None

        self.history = None

    def attach_registry(
        self,
        registry,
    ):

        self.registry = registry

    def attach_history(
        self,
        history,
    ):

        self.history = history

    def record(

        self,

        component: str,

        action: str,

        payload=None,

        user: str = "system",

    ):

        record = AuditRecord(

            component=component,

            action=action,

            payload=payload or {},

            user=user,

        )

        if self.registry:

            self.registry.register(record)

        if self.history:

            self.history.add(record)

        return record