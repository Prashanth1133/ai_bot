from __future__ import annotations

from enum import Enum


class Label(Enum):

    STRONG_SELL = 0

    SELL = 1

    HOLD = 2

    BUY = 3

    STRONG_BUY = 4


class FutureLabeler:
    """
    Creates classification labels
    using future returns.
    """

    def __init__(

        self,

        lookahead: int = 30,

        strong_buy: float = 0.03,

        buy: float = 0.01,

        sell: float = -0.01,

        strong_sell: float = -0.03,

    ):

        self.lookahead = lookahead

        self.strong_buy = strong_buy

        self.buy = buy

        self.sell = sell

        self.strong_sell = strong_sell

    ########################################################

    def label(

        self,

        closes,

        index,

    ):

        if index + self.lookahead >= len(closes):

            return None

        current = float(closes[index])

        future = float(

            closes[index + self.lookahead]

        )

        change = (

            future - current

        ) / current

        if change >= self.strong_buy:

            return Label.STRONG_BUY

        if change >= self.buy:

            return Label.BUY

        if change <= self.strong_sell:

            return Label.STRONG_SELL

        if change <= self.sell:

            return Label.SELL

        return Label.HOLD

    ########################################################

    def generate(

        self,

        dataframe,

    ):

        closes = dataframe["close"].tolist()

        labels = []

        for i in range(len(closes)):

            label = self.label(

                closes,

                i,

            )

            labels.append(

                None if label is None else label.value

            )

        dataframe = dataframe.copy()

        dataframe["label"] = labels

        dataframe = dataframe.dropna()

        dataframe.reset_index(

            drop=True,

            inplace=True,

        )

        return dataframe