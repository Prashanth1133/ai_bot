class FeatureMerger:

    def merge(

        self,

        *feature_sets

    ):

        merged = {}

        for features in feature_sets:

            merged.update(

                features

            )

        return merged