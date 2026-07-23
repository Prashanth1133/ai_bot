import os
import time
import pandas as pd

from binance.client import Client


class BinanceDownloader:

    def __init__(self):

        self.client = Client()

    #################################################

    def download(

        self,
        symbol,
        interval,
        limit=1000

    ):

        print(

            f"\nDownloading "

            f"{symbol}"

            f" -> "

            f"{interval}"

        )

        klines = (

            self.client.get_klines(

                symbol=symbol,
                interval=interval,
                limit=limit

            )

        )

        rows = []

        for k in klines:

            rows.append(

                {

                    "timestamp":k[0],

                    "open":float(k[1]),

                    "high":float(k[2]),

                    "low":float(k[3]),

                    "close":float(k[4]),

                    "volume":float(k[5])

                }

            )

        return pd.DataFrame(

            rows

        )

    #################################################

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

            f"Saved : {path}"

        )


#########################################################


if __name__ == "__main__":

    downloader = BinanceDownloader()


    symbols = [

        "BTCUSDT",

        "ETHUSDT",

        "DOGEUSDT"

    ]


    intervals = [

        Client.KLINE_INTERVAL_15MINUTE,

        Client.KLINE_INTERVAL_30MINUTE,

        Client.KLINE_INTERVAL_1HOUR,

        Client.KLINE_INTERVAL_4HOUR,

    ]


    for symbol in symbols:

        for interval in intervals:

            dataframe = (

                downloader.download(

                    symbol=symbol,

                    interval=interval,

                    limit=1000

                )

            )

            downloader.save(

                symbol,

                interval,

                dataframe

            )

            time.sleep(1)