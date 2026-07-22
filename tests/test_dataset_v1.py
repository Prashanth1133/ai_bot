from data.build_dataset import DatasetBuilder

builder = DatasetBuilder()

X, y = builder.process(

    "data/raw/BTCUSDT.csv"

)

print(X.shape)

for k, v in y.items():

    print(
        k,
        v.shape
    )