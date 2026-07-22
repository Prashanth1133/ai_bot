import os
import time

import pandas as pd
from binance.client import Client


class BinanceDownloader:

    def __init__(self):

        self.client = Client()

    def download(

        self,
        symbol,
        interval="1m",
        limit=1000

    ):

        print(

            f"Downloading {symbol}..."

        )

        klines = self.client.get_klines(

            symbol=symbol,
            interval=interval,
            limit=limit

        )

        rows = []

        for k in klines:

            rows.append(

                {

                    "timestamp": k[0],
                    "open": float(k[1]),
                    "high": float(k[2]),
                    "low": float(k[3]),
                    "close": float(k[4]),
                    "volume": float(k[5])

                }

            )

        return pd.DataFrame(

            rows

        )

    def save(

        self,
        symbol,
        df

    ):

        os.makedirs(

            "data/raw",

            exist_ok=True

        )

        path = (

            f"data/raw/{symbol}.csv"

        )

        df.to_csv(

            path,

            index=False

        )

        print(

            f"Saved: {path}"

        )


if __name__ == "__main__":

    downloader = BinanceDownloader()

    for symbol in [

        "BTCUSDT",
        "ETHUSDT",
        "DOGEUSDT"

    ]:

        df = downloader.download(

            symbol=symbol

        )

        downloader.save(

            symbol,
            df

        )

        time.sleep(1)