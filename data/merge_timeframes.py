import pandas as pd


class TimeframeMerger:


    def merge(

        self,
        datasets

    ):

        merged = []


        for timeframe in datasets:

            dataframe = (

                datasets[timeframe]

                .copy()

            )

            dataframe[

                "timeframe"

            ] = timeframe


            merged.append(

                dataframe

            )


        dataframe = pd.concat(

            merged,

            ignore_index=True

        )


        dataframe = dataframe.sort_values(

            by="time"

        )


        return dataframe.reset_index(

            drop=True

        )