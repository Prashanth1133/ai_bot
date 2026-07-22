from news.models import NewsCategory


class NewsClassifier:

    def classify(self, article):

        text = (

            article.title

            + " "

            + article.content

        ).lower()

        if "etf" in text:

            article.category = NewsCategory.ETF

        elif "hack" in text:

            article.category = NewsCategory.HACK

        elif "listing" in text:

            article.category = NewsCategory.LISTING

        elif "fomc" in text:

            article.category = NewsCategory.FOMC

        elif "fed" in text:

            article.category = NewsCategory.FED

        return article