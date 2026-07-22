class ContextStatistics:

    def __init__(self):

        self.snapshots = 0

    def update(self):

        self.snapshots += 1

    def statistics(self):

        return {

            "snapshots": self.snapshots,

        }