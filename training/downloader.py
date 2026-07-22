from pathlib import Path

import pandas as pd

import requests


class BinanceDownloader:

    BASE = "https://data.binance.vision"

    def download(

        self,

        symbol,

        interval,

        year,

        month

    ):

        filename = f"{symbol}-{interval}-{year}-{month:02}.zip"

        url = (

            f"{self.BASE}/"

            f"data/spot/monthly/klines/"

            f"{symbol}/{interval}/{filename}"

        )

        output = Path("historical")

        output.mkdir(exist_ok=True)

        path = output / filename

        if path.exists():

            return path

        response = requests.get(url)

        path.write_bytes(response.content)

        return path