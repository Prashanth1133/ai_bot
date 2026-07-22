from feature_store.merger import FeatureMerger


class FeatureProcessor:

    def __init__(self):

        self.merger = FeatureMerger()

    def process(

        self,

        *feature_sets

    ):

        return self.merger.merge(

            *feature_sets

        )