import json


class StateSerializer:

    @staticmethod
    def serialize(state):

        return json.dumps(state)

    @staticmethod
    def deserialize(data):

        return json.loads(data)
        