from data.build_dataset import DatasetBuilder
from data.crypto_dataset import CryptoDataset

from torch.utils.data import DataLoader


builder = DatasetBuilder()

X, y = builder.process(
    "data/raw/BTCUSDT.csv"
)

dataset = CryptoDataset(
    X,
    y
)

loader = DataLoader(
    dataset,
    batch_size=8,
    shuffle=True
)

x, target = next(iter(loader))

print("X:", x.shape)

for k, v in target.items():

    print(
        k,
        v.shape,
        v.dtype
    )