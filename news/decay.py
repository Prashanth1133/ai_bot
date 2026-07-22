from datetime import datetime
import math


class NewsDecay:

    HALF_LIFE_HOURS = 24

    def score(self, article):

        hours = (

            datetime.utcnow()

            - article.published

        ).total_seconds() / 3600

        decay = math.exp(

            -hours /

            self.HALF_LIFE_HOURS

        )

        return decay