import re


class EntityExtractor:

    SYMBOLS = {

        "BTC",

        "ETH",

        "SOL",

        "DOGE",

        "BNB",

        "XRP",

        "ADA"

    }

    def extract(self, article):

        text = (
            article.title
            + " "
            + article.content
        ).upper()

        assets = []

        for symbol in self.SYMBOLS:

            if re.search(rf"\b{symbol}\b", text):

                assets.append(symbol)

        article.affected_assets = assets

        return article