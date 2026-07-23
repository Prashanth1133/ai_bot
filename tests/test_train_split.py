from training.train_validation_split import (
    TrainValidationSplit
)

import numpy as np


X = np.random.rand(

    100,
    128,
    11

)


y = {

    "direction":

    np.random.randint(

        0,
        3,
        100

    )

}


result = (

    TrainValidationSplit()

    .split(

        X,
        y

    )

)


print(

    len(result)

)