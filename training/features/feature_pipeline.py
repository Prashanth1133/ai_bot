from training.features.feature_validator import FeatureValidator
from training.features.feature_normalizer import FeatureNormalizer
from training.features.feature_selector import FeatureSelector


class FeaturePipeline:

    def __init__(self):

        self.validator = FeatureValidator()

        self.normalizer = FeatureNormalizer()

        self.selector = FeatureSelector()

    def process(

        self,

        dataframe,

    ):

        dataframe = self.validator.validate(
            dataframe
        )

        self.normalizer.fit(
            dataframe
        )

        dataframe = self.normalizer.transform(
            dataframe
        )

        dataframe = self.selector.select(
            dataframe
        )

        return dataframe