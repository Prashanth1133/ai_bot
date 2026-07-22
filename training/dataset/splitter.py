class TimeSeriesSplitter:

    """
    Splits data chronologically.
    """

    def split(

        self,

        samples,

        train=0.70,

        valid=0.15

    ):

        n = len(samples)

        train_end = int(n * train)

        valid_end = int(n * (train + valid))

        return (

            samples[:train_end],

            samples[train_end:valid_end],

            samples[valid_end:]

        )