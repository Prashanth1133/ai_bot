from __future__ import annotations

import hashlib
import random

from news.models import NewsArticle


class NewsEmbedding:
    """
    Temporary embedding generator.

    Replace with SentenceTransformer
    later.
    """

    def __init__(self):

        self.dimension = 384

    def encode(self, article: NewsArticle):

        seed = int(
            hashlib.md5(
                article.title.encode()
            ).hexdigest(),
            16
        )

        rng = random.Random(seed)

        article.embedding = [

            rng.uniform(-1, 1)

            for _ in range(self.dimension)

        ]

        return article