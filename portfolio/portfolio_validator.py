class PortfolioValidator:

    @staticmethod
    def validate(snapshot):

        if snapshot is None:

            return False

        if snapshot.equity < 0:

            return False

        if snapshot.cash < 0:

            return False

        return True