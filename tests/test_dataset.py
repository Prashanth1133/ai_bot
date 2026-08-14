from data.build_dataset import DatasetBuilder

def test_dataset_builder_uses_available_btc_data():
    X, y = DatasetBuilder().process("data/raw/BTCUSDT_15m.csv")
    assert len(X) == len(y["direction"])
    assert X.shape[-1] == 11
