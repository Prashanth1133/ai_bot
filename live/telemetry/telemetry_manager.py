from live.telemetry.telemetry_record import (
    TelemetryRecord,
)


class TelemetryManager:

    def __init__(

        self,

        registry,

        history=None,

    ):

        self.registry = registry

        self.history = history

    def publish(

        self,

        component,

        metric,

        value,

        unit="",

        labels=None,

    ):

        record = TelemetryRecord(

            component=component,

            metric=metric,

            value=value,

            unit=unit,

            labels=labels or {},

        )

        self.registry.update(record)

        if self.history:

            self.history.add(record)

        return record