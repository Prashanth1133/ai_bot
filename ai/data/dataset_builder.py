from ai.data.sequence_builder import SequenceBuilder


class DatasetBuilder:

    def __init__(self):

        self.builder = SequenceBuilder()

    def build(

        self,

        features,

        labels

    ):

        return self.builder.build(

            features,

            labels

        )