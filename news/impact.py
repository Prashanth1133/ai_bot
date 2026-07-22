from __future__ import annotations

from news.models import (
    NewsArticle,
    NewsCategory,
    Sentiment,
)


class NewsImpactScorer:
    """
    Calculates the expected market impact
    of a news article.
    """

    CATEGORY_SCORE = {

        NewsCategory.HACK: 9.5,

        NewsCategory.REGULATION: 9.0,

        NewsCategory.FOMC: 10.0,

        NewsCategory.FED: 10.0,

        NewsCategory.CPI: 9.8,

        NewsCategory.ETF: 9.2,

        NewsCategory.LISTING: 7.5,

        NewsCategory.DELISTING: 8.5,

        NewsCategory.PARTNERSHIP: 6.0,

        NewsCategory.WHALE: 7.8,

        NewsCategory.MACRO: 8.8,

        NewsCategory.UNKNOWN: 4.0,
    }

    SENTIMENT_MULTIPLIER = {

        Sentiment.VERY_BEARISH: 1.20,

        Sentiment.BEARISH: 1.10,

        Sentiment.NEUTRAL: 1.00,

        Sentiment.BULLISH: 1.10,

        Sentiment.VERY_BULLISH: 1.20,
    }

    def score(self, article: NewsArticle):

        base = self.CATEGORY_SCORE.get(
            article.category,
            4.0
        )

        multiplier = self.SENTIMENT_MULTIPLIER.get(
            article.sentiment,
            1.0
        )

        article.impact = round(
            min(base * multiplier, 10.0),
            2
        )

        return article