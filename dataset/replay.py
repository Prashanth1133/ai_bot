class ReplayBuffer:

    def __init__(self):

        self.samples = []

    def add(

        self,

        sequence

    ):

        self.samples.append(sequence)

    def clear(self):

        self.samples.clear()

    def __len__(self):

        return len(self.samples)