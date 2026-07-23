import numpy as np


class EarlyStopping:

    def __init__(

        self,
        patience=25,
        min_delta=0.0001

    ):

        self.patience = patience

        self.min_delta = min_delta

        self.best_loss = np.inf

        self.counter = 0

        self.stop_training = False


    def __call__(

        self,
        validation_loss

    ):


        if (

            validation_loss
            <
            (self.best_loss - self.min_delta)

        ):

            self.best_loss = validation_loss

            self.counter = 0

            return False


        self.counter += 1


        print(

            f"EarlyStopping Counter : "

            f"{self.counter}/"

            f"{self.patience}"

        )


        if (

            self.counter
            >=
            self.patience

        ):

            self.stop_training = True

            print(

                "\nEarly Stopping Activated."

            )

            return True


        return False


    def reset(self):

        self.counter = 0

        self.best_loss = np.inf

        self.stop_training = False