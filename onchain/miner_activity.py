class MinerActivity:

    def classify(self, event):

        if event.event_type == "miner_sell":

            return -1

        if event.event_type == "miner_buy":

            return 1

        return 0