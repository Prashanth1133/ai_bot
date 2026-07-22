class TwitterProcessor:

    def process(self, post):

        score = (

            post.likes

            + post.reposts * 3

            + post.replies * 2

        )

        return score