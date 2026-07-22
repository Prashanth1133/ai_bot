from training.dataloader import LiveSequenceGenerator

from features.registry import FEATURE_LIST


class SequenceProcessor:

    def __init__(self, bus):

        self.bus = bus

        self.generator = LiveSequenceGenerator(

            FEATURE_LIST,

            window=120

        )

    async def on_feature_vector(self, vector):

        sequence = self.generator.update(vector)

        if sequence is None:

            return

        await self.bus.publish(

            "feature_sequence",

            sequence

        )