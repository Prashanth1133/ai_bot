class StateValidator:

    @staticmethod
    def validate(state):

        return isinstance(state, dict)