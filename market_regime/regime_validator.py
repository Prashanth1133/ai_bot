class RegimeValidator:

    @staticmethod
    def validate(snapshot):

        if snapshot is None:

            return False

        if snapshot.confidence < 0:

            return False

        if snapshot.confidence > 1:

            return False

        return True