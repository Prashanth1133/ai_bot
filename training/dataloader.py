from training.encoder import FeatureEncoder
from training.sequence_builder import SequenceBuilder


class LiveSequenceGenerator:

    def __init__(

        self,

        feature_order,

        window=120

    ):

        self.encoder = FeatureEncoder(

            feature_order

        )

        self.sequence = SequenceBuilder(

            window

        )

    def update(

        self,

        feature_dict

    ):

        encoded = self.encoder.encode(

            feature_dict

        )

        return self.sequence.update(

            encoded

        )