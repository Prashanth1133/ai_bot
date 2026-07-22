from training.dataset.schema import DatasetSample


class DatasetBuilder:

    """
    Builds training samples from
    feature sequences and labels.
    """

    def build(

        self,

        sequence,

        label,

        symbol,

        timeframe,

        timestamp

    ):

        return DatasetSample(

            sequence=sequence,

            direction=label.direction,

            confidence=label.confidence,

            tp=label.tp,

            sl=label.sl,

            regime=label.regime,

            timestamp=timestamp,

            symbol=symbol,

            timeframe=timeframe

        )