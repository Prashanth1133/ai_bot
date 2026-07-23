import numpy as np

from training.combine_dataset import (
    CombinedDatasetBuilder
)


builder = CombinedDatasetBuilder()


X1 = np.random.rand(
    100,
    128,
    11
)

X2 = np.random.rand(
    100,
    128,
    11
)

X3 = np.random.rand(
    100,
    128,
    11
)


y1 = {

    "direction":

    np.random.randint(
        0,
        3,
        100
    )

}


y2 = {

    "direction":

    np.random.randint(
        0,
        3,
        100
    )

}


y3 = {

    "direction":

    np.random.randint(
        0,
        3,
        100
    )

}


X, y = builder.combine(

    [

        (X1, y1),

        (X2, y2),

        (X3, y3)

    ]

)


builder.information(

    X,
    y

)


print(

    X.shape

)


print(

    y["direction"].shape

)