from data.build_dataset import DatasetBuilder
from data.crypto_dataset import CryptoDataset

from ai.model import TradingTransformer
from ai.trainer import Trainer


def main():

    print("Loading ETHUSDT...")

    X, y = DatasetBuilder().process(
        "data/raw/ETHUSDT.csv"
    )

    print(f"Dataset Size: {len(X)}")

    dataset = CryptoDataset(
        X,
        y
    )

    model = TradingTransformer(
        input_dim=X.shape[-1]
    )

    trainer = Trainer(
        model=model,
        dataset=dataset,
        save_path="models/eth_v1.pt"
    )

    trainer.train(
        epochs=50
    )


if __name__ == "__main__":
    main()