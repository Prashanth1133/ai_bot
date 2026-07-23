import torch


class LearningRateScheduler:

    def __init__(

        self,
        optimizer,
        patience=5,
        factor=0.5,
        minimum_lr=1e-7

    ):


        self.optimizer = optimizer


        self.scheduler = (

            torch.optim

            .lr_scheduler

            .ReduceLROnPlateau(

                optimizer,

                mode="min",

                factor=factor,

                patience=patience,

                min_lr=minimum_lr,

                verbose=True

            )

        )


    def step(

        self,
        validation_loss

    ):


        self.scheduler.step(

            validation_loss

        )


    def get_lr(self):


        for group in (

            self.optimizer

            .param_groups

        ):

            return group["lr"]


    def print_lr(self):


        print(

            f"Current Learning Rate : "

            f"{self.get_lr()}"

        )