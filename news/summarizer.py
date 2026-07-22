class NewsSummarizer:
    """
    Placeholder summarizer.

    Later this will call
    an LLM.
    """

    def summarize(self, article):

        if article.summary:

            return article.summary

        text = article.content.strip()

        return text[:300]