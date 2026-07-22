from __future__ import annotations


class TimeSeriesSplit:

    """
    Expanding window split.
    """

    def split(

        self,

        dataframe,

        train_size=0.70,

        step=0.05,

    ):

        total = len(dataframe)

        train_end = int(total * train_size)

        step_size = int(total * step)

        while train_end + step_size < total:

            train = dataframe.iloc[:train_end]

            test = dataframe.iloc[

                train_end:

                train_end + step_size

            ]

            yield train, test

            train_end += step_size