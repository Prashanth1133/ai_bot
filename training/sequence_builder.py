from training.window import SlidingWindow


class SequenceBuilder:

    def __init__(

        self,

        window=128,

    ):

        self.window = SlidingWindow(window)

    ########################################################

    def create(

        self,

        features,

        labels,

    ):

        return self.window.build(

            features,

            labels,

        )