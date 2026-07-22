class DrawdownGuard:

    def __init__(self):

        self.max_equity = 0

    def update(

        self,

        equity

    ):

        self.max_equity = max(

            self.max_equity,

            equity

        )

        return (

            self.max_equity -

            equity

        ) / self.max_equity