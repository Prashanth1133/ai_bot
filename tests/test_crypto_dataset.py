from data.build_dataset import DatasetBuilder
from data.crypto_dataset import CryptoDataset

builder = DatasetBuilder()

X, y = builder.process(
    "data/raw/BTCUSDT.csv"
)

dataset = CryptoDataset(
    X,
    y
)

x, target = dataset[0]

print(x.shape)

for k, v in target.items():

    print(
        k,
        v,
        v.dtype
    )