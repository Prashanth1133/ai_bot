from collections import defaultdict


class EventTracker:

    def __init__(self):

        self.events = defaultdict(list)

    def add(self, article):

        key = (

            article.category,

            tuple(

                sorted(

                    article.affected_assets

                )

            )

        )

        self.events[key].append(

            article

        )

    def active_events(self):

        return self.events