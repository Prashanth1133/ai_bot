import numpy as np


class LabelBuilder:

    def build(
        self,
        closes,
        lookahead=5,
        threshold=0.002
    ):

        labels = []

        for i in range(len(closes)):

            if i + lookahead >= len(closes):

                labels.append(1)
                continue

            current = closes[i]

            future = closes[
                i + lookahead
            ]

            change = (

                future - current

            ) / current

            if change > threshold:

                labels.append(2)  # BUY

            elif change < -threshold:

                labels.append(0)  # SELL

            else:

                labels.append(1)  # HOLD

        return np.array(
            labels,
            dtype=np.int64
        )