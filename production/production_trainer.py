import torch


class ProductionTrainer:


    def __init__(

        self,
        trainer

    ):

        self.trainer = trainer


    def train(

        self,
        epochs=100

    ):


        print(

            "\nProduction Training Started\n"

        )


        self.trainer.train(

            epochs=epochs

        )


        print(

            "\nProduction Training Finished\n"

        )