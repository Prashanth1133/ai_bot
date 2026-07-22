from sentiment.embedding import SocialEmbedding
from sentiment.feature_builder import SentimentFeatureBuilder
from sentiment.influencer_tracker import InfluencerTracker


class SentimentProcessor:

    def __init__(self):

        self.embedding = SocialEmbedding()

        self.builder = SentimentFeatureBuilder()

        self.influencer = InfluencerTracker()

    def process(self, post):

        influence = self.influencer.score(

            post.author

        )

        engagement = (

            post.likes

            + post.reposts

            + post.replies

        )

        post.embedding = self.embedding.encode(

            post.text

        )

        return self.builder.build(

            post,

            influence,

            engagement

        )