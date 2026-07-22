class RedditProcessor:

    def process(self, submission):

        return (

            submission.score

            + submission.comments * 2

        )