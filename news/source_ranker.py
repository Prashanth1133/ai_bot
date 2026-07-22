from __future__ import annotations


class SourceRanker:

    """
    Reliability score of each source.
    """

    SCORES = {

        "Reuters": 10.0,

        "Bloomberg": 9.9,

        "Federal Reserve": 10.0,

        "SEC": 10.0,

        "Binance": 9.5,

        "CoinDesk": 9.0,

        "CoinTelegraph": 8.7,

        "CryptoPanic": 8.0,

        "Twitter": 6.0,

        "Reddit": 5.5,

        "Telegram": 5.0
    }

    def score(self, article):

        article.confidence = self.SCORES.get(

            article.source,

            5.0

        )

        return article