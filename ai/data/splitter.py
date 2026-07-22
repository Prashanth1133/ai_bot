class WalkForwardSplitter:

    def split(

        self,

        data,

        train=0.70,

        valid=0.15

    ):

        n = len(data)

        train_end = int(n * train)

        valid_end = int(n * (train + valid))

        return (

            data[:train_end],

            data[train_end:valid_end],

            data[valid_end:]

        )