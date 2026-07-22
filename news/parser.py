import re


class NewsParser:

    def clean(self, text: str) -> str:

        text = re.sub(r"\s+", " ", text)

        return text.strip()

    def parse(self, article):

        article.title = self.clean(article.title)

        article.summary = self.clean(article.summary)

        article.content = self.clean(article.content)

        return article