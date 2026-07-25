import os
import time
import pandas as pd

from datetime import datetime

from binance.client import Client


class BinanceDownloader:

    def __init__(self):

        self.client = Client()

    #####################################################

    def download(

        self,
        symbol,
        interval,
        start_str="1 year ago UTC"

    ):

        print()

        print("=" * 60)

        print(

            f"Downloading "

            f"{symbol}"

            f" -> "

            f"{interval}"

        )

        print(

            f"Start Date : "

            f"{start_str}"

        )

        print()

        klines = (

            self.client.get_historical_klines(

                symbol=symbol,

                interval=interval,

                start_str=start_str,

            )

        )

        rows = []


        for k in klines:

            rows.append(

                {

                    "timestamp":

                    pd.to_datetime(

                        k[0],

                        unit="ms"

                    ),

                    "open":

                    float(k[1]),

                    "high":

                    float(k[2]),

                    "low":

                    float(k[3]),

                    "close":

                    float(k[4]),

                    "volume":

                    float(k[5]),

                }

            )


        dataframe = (

            pd.DataFrame(

                rows

            )

        )


        print(

            f"Downloaded : "

            f"{len(dataframe)} "

            f"candles"

        )


        return dataframe


    #####################################################


    def save(

        self,
        symbol,
        interval,
        dataframe

    ):


        os.makedirs(

            "data/raw",

            exist_ok=True

        )


        path = (

            f"data/raw/"

            f"{symbol}_"

            f"{interval}.csv"

        )


        dataframe.to_csv(

            path,

            index=False

        )


        print(

            f"Saved : "

            f"{path}"

        )


    #####################################################


    def download_and_save(

        self,
        symbol,
        interval,
        start_str="1 year ago UTC"

    ):


        dataframe = (

            self.download(

                symbol=symbol,

                interval=interval,

                start_str=start_str

            )

        )


        self.save(

            symbol,

            interval,

            dataframe

        )


        return dataframe


#########################################################


if __name__ == "__main__":


    downloader = BinanceDownloader()


    symbols = [

        "BTCUSDT",

        "ETHUSDT",

        "DOGEUSDT",

    ]


    intervals = [

        Client.KLINE_INTERVAL_15MINUTE,

        Client.KLINE_INTERVAL_30MINUTE,

        Client.KLINE_INTERVAL_1HOUR,

        Client.KLINE_INTERVAL_4HOUR,

    ]


    #################################################

    # OPTIONS
    #
    # 1 year ago UTC
    # 2 years ago UTC
    # 3 years ago UTC
    #
    #################################################

    START_DATE = (

        "1 year ago UTC"

    )


    for symbol in symbols:


        for interval in intervals:


            downloader.download_and_save(

                symbol=symbol,

                interval=interval,

                start_str=START_DATE,

            )


            time.sleep(1)


    print()

    print("=" * 60)

    print("ALL DOWNLOADS COMPLETED")

    print("=" * 60)

    print()