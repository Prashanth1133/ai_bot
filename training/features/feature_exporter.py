class FeatureExporter:

    def export(

        self,

        dataframe,

        path,

    ):

        dataframe.to_parquet(

            path,

            index=False,

        )