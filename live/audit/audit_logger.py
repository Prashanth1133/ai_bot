from live.audit.audit_event import AuditEvent


class AuditLogger:

    def __init__(

        self,

        registry,

        history=None,

    ):

        self.registry = registry

        self.history = history

    def log(

        self,

        category: str,

        action: str,

        component: str,

        success: bool = True,

        message: str = "",

        metadata=None,

        user: str = "system",

    ):

        event = AuditEvent(

            category=category,

            action=action,

            component=component,

            success=success,

            message=message,

            metadata=metadata or {},

            user=user,

        )

        self.registry.add(event)

        if self.history:

            self.history.add(event)

        return event