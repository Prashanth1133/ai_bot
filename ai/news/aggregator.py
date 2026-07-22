import feedparser

SOURCES = [

    "https://www.coindesk.com/arc/outboundfeeds/rss/",

    "https://cointelegraph.com/rss",

]


class NewsAggregator:

    def fetch(self):

        articles = []

        for url in SOURCES:

            feed = (
                feedparser.parse(
                    url
                )
            )

            for item in (
                feed.entries
            ):

                articles.append(
                    {
                        "title":
                        item.title,

                        "summary":
                        item.summary
                    }
                )

        return articles