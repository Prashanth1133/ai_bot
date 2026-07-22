class DatasetValidator:

    def validate(self, sample):

        if sample.sequence is None:
            return False

        if len(sample.sequence) == 0:
            return False

        if sample.direction not in [0, 1, 2]:
            return False

        return True