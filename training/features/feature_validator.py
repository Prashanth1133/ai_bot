class FeatureValidator:

    def validate(

        self,

        dataframe,

    ):

        dataframe = dataframe.dropna()

        dataframe = dataframe.replace(

            [float("inf"), -float("inf")],

            0,

        )

        return dataframe