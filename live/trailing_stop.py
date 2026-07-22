class TrailingStop:

    def __init__(

        self,
        trail_percent=0.01

    ):

        self.trail_percent = (

            trail_percent

        )

        self.stop = None

    def update(

        self,
        price

    ):

        new_stop = (

            price *

            (1 - self.trail_percent)

        )

        if self.stop is None:

            self.stop = new_stop

        else:

            self.stop = max(

                self.stop,
                new_stop

            )

        return self.stop