from feature_fusion.feature_vector import (
    FeatureVector
)

from feature_fusion.normalizer import (
    FeatureNormalizer
)


class FeatureFusionEngine:

    def __init__(self):

        self.normalizer = FeatureNormalizer()

    def build(

        self,

        symbol,

        timeframe,

        timestamp,

        modules

    ):

        fv = FeatureVector(

            symbol,

            timeframe,

            timestamp

        )

        for module in modules:

            if module is None:

                continue

            if isinstance(module, dict):

                for k, v in module.items():

                    fv.add(k, v)

            elif hasattr(module, "__dict__"):

                for k, v in vars(module).items():

                    fv.add(k, v)

        return self.normalizer.normalize(

            fv.get()

        )