class MetricsTracker:

    def __init__(self):

        self.history = []

    ###########################################################

    def add(

        self,

        metrics,

    ):

        self.history.append(metrics)

    ###########################################################

    def average(self):

        if not self.history:

            return {}

        keys = self.history[0].keys()

        return {

            k: sum(

                m[k]

                for m in self.history

            ) / len(self.history)

            for k in keys

        }