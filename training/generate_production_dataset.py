import os

from training.combine_dataset import (
    CombinedDatasetBuilder
)

from training.save_dataset import (
    save_dataset
)


DATA_FILES = [

    "BTCUSDT_15m.csv",
    "BTCUSDT_30m.csv",
    "BTCUSDT_1h.csv",
    "BTCUSDT_4h.csv",

    "ETHUSDT_15m.csv",
    "ETHUSDT_30m.csv",
    "ETHUSDT_1h.csv",
    "ETHUSDT_4h.csv",

    "DOGEUSDT_15m.csv",
    "DOGEUSDT_30m.csv",
    "DOGEUSDT_1h.csv",
    "DOGEUSDT_4h.csv",

]


def main():

    builder = CombinedDatasetBuilder()

    datasets = []

    print("\n")

    print("=" * 60)
    print("LOADING DATASETS")
    print("=" * 60)

    for file_name in DATA_FILES:

        path = os.path.join(
            "data",
            "raw",
            file_name
        )

        print(f"\nLoading -> {file_name}")

        datasets.append(

            builder.load(
                path
            )

        )

    print("\n")
    print("=" * 60)
    print("COMBINING DATASETS")
    print("=" * 60)

    X, y = builder.combine(
        datasets
    )

    X, y = builder.shuffle(
        X,
        y
    )

    builder.information(
        X,
        y
    )

    data = {

        "X": X,
        "y": y

    }

    save_dataset(

        "data/processed/combined.npy",

        data

    )

    print("\n")
    print("=" * 60)
    print("PRODUCTION DATASET READY")
    print("=" * 60)
    print("\n")


if __name__ == "__main__":

    main()