class StateDiff:

    @staticmethod
    def compare(

        previous: dict,

        current: dict,

    ):

        changes = {}

        previous = previous or {}

        current = current or {}

        keys = set(previous) | set(current)

        for key in keys:

            if previous.get(key) != current.get(key):

                changes[key] = {

                    "old": previous.get(key),

                    "new": current.get(key),

                }

        return changes