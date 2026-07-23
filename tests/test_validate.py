import torch

from evaluation.metrics import (
    Metrics
)


prediction = torch.tensor(

    [

        [0.1,0.3,0.6],

        [0.8,0.1,0.1]

    ]

)


target = torch.tensor(

    [

        2,
        0

    ]

)


accuracy = (

    Metrics.direction_accuracy(

        prediction,

        target

    )

)


print(

    "\nAccuracy :",

    accuracy

)