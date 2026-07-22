import numpy as np


class NewsFeatureBuilder:

    def build(self, article):

        features = {

            "impact":

                article.impact,

            "sentiment":

                article.sentiment.value,

            "asset_count":

                len(article.affected_assets),

            "embedding":

                np.array(
                    article.embedding,
                    dtype=np.float32
                ),
        }

        return features