from data.build_dataset import DatasetBuilder
from data.crypto_dataset import CryptoDataset

from torch.utils.data import DataLoader


def test_dataloader_batches_crypto_dataset():
    X, y = DatasetBuilder().process("data/raw/BTCUSDT_15m.csv")
    loader = DataLoader(CryptoDataset(X, y), batch_size=8, shuffle=False)
    x, target = next(iter(loader))
    assert x.shape[-1] == 11
    assert x.shape[0] <= 8
    assert "direction" in target
