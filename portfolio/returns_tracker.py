class ReturnsTracker:

    def __init__(self):

        self.previous = None

    def update(

        self,

        equity,

    ):

        if self.previous is None:

            self.previous = equity

            return 0.0

        if self.previous == 0:

            return 0.0

        ret = (

            equity - self.previous

        ) / self.previous

        self.previous = equity

        return ret