class WalkForwardValidator:

    def split(

        self,

        dataframe,

        train_size,

    ):

        split = int(

            len(dataframe)

            * train_size

        )

        return (

            dataframe[:split],

            dataframe[split:],

        )