from collections import deque


class TradeMemory:

    """
    Stores recent AI decisions for
    self-evaluation.
    """

    def __init__(

        self,

        max_size=5000,

    ):

        self.memory = deque(
            maxlen=max_size
        )

    def add(

        self,

        trade,

    ):

        self.memory.append(trade)

    def last(self, n=100):

        return list(self.memory)[-n:]