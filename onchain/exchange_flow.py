class ExchangeFlow:

    def classify(self, event):

        if event.exchange is None:

            return None

        if event.to_address.startswith("exchange"):

            return "INFLOW"

        if event.from_address.startswith("exchange"):

            return "OUTFLOW"

        return None