import hashlib


class NewsDeduplicator:

    def __init__(self):

        self.cache = set()

    def is_duplicate(self, article):

        text = (

            article.title

            + article.summary

        ).lower()

        fingerprint = hashlib.sha256(

            text.encode()

        ).hexdigest()

        if fingerprint in self.cache:

            return True

        self.cache.add(

            fingerprint

        )

        return False