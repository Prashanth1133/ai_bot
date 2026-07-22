from feature_fusion.fusion_result import FusionResult


class FusionPipeline:

    def __init__(

        self,

        registry,

        normalizer,

    ):

        self.registry = registry

        self.normalizer = normalizer

    def run(

        self,

        context,

    ):

        names = []

        values = []

        for name, extractor in self.registry.all():

            feature = extractor(context)

            names.extend(feature.names)

            values.extend(feature.values)

        vector = self.normalizer.normalize(values)

        return FusionResult(

            symbol=context.symbol,

            vector=vector,

            feature_names=names,

        )