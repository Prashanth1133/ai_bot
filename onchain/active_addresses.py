class ActiveAddressTracker:

    def score(self,

              current,

              previous):

        if previous == 0:

            return 0

        return (

            current

            - previous

        ) / previous