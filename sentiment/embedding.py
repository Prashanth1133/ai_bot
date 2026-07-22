import hashlib
import random


class SocialEmbedding:

    def encode(self, text):

        seed = int(

            hashlib.md5(

                text.encode()

            ).hexdigest(),

            16

        )

        rng = random.Random(seed)

        return [

            rng.uniform(-1,1)

            for _ in range(384)

        ]