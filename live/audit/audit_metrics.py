from __future__ import annotations

from collections import defaultdict


class AuditMetrics:

    def __init__(self):

        self.records = 0

        self.actions = defaultdict(int)

        self.components = defaultdict(int)

    def update(
        self,
        record,
    ):

        self.records += 1

        self.actions[
            record.action
        ] += 1

        self.components[
            record.component
        ] += 1