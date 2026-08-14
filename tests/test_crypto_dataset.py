from data.build_dataset import DatasetBuilder
from data.crypto_dataset import CryptoDataset

def test_crypto_dataset_exposes_tensor_targets():
    X, y = DatasetBuilder().process("data/raw/BTCUSDT_15m.csv")
    x, target = CryptoDataset(X, y)[0]
    assert x.shape[-1] == 11
    assert set(target) == set(y)
