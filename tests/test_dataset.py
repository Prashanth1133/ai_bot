from data.build_dataset import DatasetBuilder

builder = DatasetBuilder()

X, y = builder.process(

    "data/raw/BTCUSDT.csv"

)

print(

    X.shape

)

print(

    y.shape

)