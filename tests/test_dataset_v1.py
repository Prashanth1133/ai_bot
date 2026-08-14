from data.build_dataset import DatasetBuilder

def test_dataset_labels_align_with_sequences():
    X, y = DatasetBuilder().process("data/raw/BTCUSDT_15m.csv")
    assert all(len(values) == len(X) for values in y.values())
