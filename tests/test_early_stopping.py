from training.early_stopping import (
    EarlyStopping
)


stopper = EarlyStopping()


losses = [

    10,
    8,
    5,
    4,
    3,
    2,
    1

]


for loss in losses:

    print(

        stopper.stop(

            loss

        )

    )