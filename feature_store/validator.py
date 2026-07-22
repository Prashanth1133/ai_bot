class FeatureValidator:

    REQUIRED = {

        "timestamp",

        "symbol",

        "source",

        "features"

    }

    def validate(

        self,

        record

    ):

        return all(

            hasattr(

                record,

                field

            )

            for field in self.REQUIRED
        )