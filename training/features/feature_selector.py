class FeatureSelector:

    """
    Remove columns that should never
    be given to the model.
    """

    DROP_COLUMNS = [

        "timestamp",

        "symbol",

        "target",

    ]

    def select(

        self,

        dataframe,

    ):

        cols = [

            c

            for c in dataframe.columns

            if c not in self.DROP_COLUMNS

        ]

        return dataframe[cols]