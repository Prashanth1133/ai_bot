import numpy as np

from training.combine_dataset import (
    CombinedDatasetBuilder
)

from training.save_dataset import (
    save_dataset
)


def main():

    builder = CombinedDatasetBuilder()


    print("\nLoading BTC Dataset...")

    btc = builder.load(

        "data/raw/BTCUSDT.csv"

    )


    print("\nLoading ETH Dataset...")

    eth = builder.load(

        "data/raw/ETHUSDT.csv"

    )


    print("\nLoading DOGE Dataset...")

    doge = builder.load(

        "data/raw/DOGEUSDT.csv"

    )


    print("\nCombining Datasets...")


    X,y = builder.combine(

        [

            btc,
            eth,
            doge

        ]

    )


    print(

        f"Combined Dataset : {len(X)}"

    )


    X,y = builder.shuffle(

        X,
        y

    )


    data = {

        "X":X,
        "y":y

    }


    save_dataset(

        "data/processed/combined.npy",

        data

    )


    print(

        "\nProduction Dataset Ready."

    )


if __name__ == "__main__":

    main()