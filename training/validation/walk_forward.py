from training.validation.time_series_split import TimeSeriesSplit
from training.validation.metrics_tracker import MetricsTracker


class WalkForwardValidation:

    def __init__(self):

        self.splitter = TimeSeriesSplit()

        self.metrics = MetricsTracker()

    ###########################################################

    def run(

        self,

        dataframe,

        trainer,

    ):

        for train_df, test_df in self.splitter.split(

            dataframe

        ):

            trainer.train(

                feature_dataframe=train_df

            )

        return self.metrics.average()