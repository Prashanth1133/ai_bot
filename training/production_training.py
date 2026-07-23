from data.build_dataset import DatasetBuilder

from data.crypto_dataset import CryptoDataset

from training.merge_dataset import MergeDataset

from ai.model import TradingTransformer

from ai.trainer import Trainer


def main():


    print(

        "\nLoading Datasets..."

    )


    btc = DatasetBuilder().process(

        "data/raw/BTCUSDT.csv"

    )


    eth = DatasetBuilder().process(

        "data/raw/ETHUSDT.csv"

    )


    doge = DatasetBuilder().process(

        "data/raw/DOGEUSDT.csv"

    )


    X, y = MergeDataset.merge(

        [

            btc,
            eth,
            doge

        ]

    )


    print(

        "\nTotal Samples :",

        len(X)

    )


    dataset = CryptoDataset(

        X,
        y

    )


    model = TradingTransformer(

        input_dim=X.shape[-1]

    )


    trainer = Trainer(

        model=model,
        dataset=dataset

    )


    trainer.train(

        epochs=200

    )


if __name__ == "__main__":

    main()