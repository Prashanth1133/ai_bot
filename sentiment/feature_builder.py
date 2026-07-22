import numpy as np


class SentimentFeatureBuilder:

    def build(

        self,

        post,

        influence,

        engagement

    ):

        return {

            "sentiment":

                post.sentiment,

            "influence":

                influence,

            "engagement":

                engagement,

            "embedding":

                np.array(

                    post.embedding,

                    dtype=np.float32

                )
        }