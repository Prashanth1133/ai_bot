from datetime import datetime

from live.statistics.statistic import Statistic


class StatisticManager:

    def __init__(

        self,

        registry,

        history=None,

    ):

        self.registry = registry

        self.history = history

    def update(

        self,

        name,

        value,

        unit="",

        metadata=None,

    ):

        statistic = Statistic(

            name=name,

            value=value,

            unit=unit,

            metadata=metadata or {},

            updated_at=datetime.utcnow(),

        )

        self.registry.update(
            statistic
        )

        if self.history:

            self.history.add(
                statistic
            )

        return statistic