from news.parser import NewsParser
from news.entity_extractor import EntityExtractor
from news.classifier import NewsClassifier
from news.impact import NewsImpactScorer
from news.summarizer import NewsSummarizer
from news.embedding import NewsEmbedding
from news.feature_builder import NewsFeatureBuilder


class NewsProcessor:

    def __init__(self):

        self.parser = NewsParser()

        self.entities = EntityExtractor()

        self.classifier = NewsClassifier()

        self.impact = NewsImpactScorer()

        self.summary = NewsSummarizer()

        self.embedding = NewsEmbedding()

        self.builder = NewsFeatureBuilder()

    def process(self, article):

        article = self.parser.parse(article)

        article = self.entities.extract(article)

        article = self.classifier.classify(article)

        article = self.impact.score(article)

        article.summary = self.summary.summarize(article)

        article = self.embedding.encode(article)

        return self.builder.build(article)