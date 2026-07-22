from collections import defaultdict


class NotificationMetrics:

    def __init__(self):

        self.sent = defaultdict(int)

        self.failed = defaultdict(int)

    def record_sent(
        self,
        channel: str,
    ):

        self.sent[channel] += 1

    def record_failed(
        self,
        channel: str,
    ):

        self.failed[channel] += 1

    def statistics(self):

        return {

            "sent": dict(self.sent),

            "failed": dict(self.failed),

        }