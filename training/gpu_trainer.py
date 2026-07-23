import torch


class GPUTrainer:


    @staticmethod

    def device():


        if torch.cuda.is_available():

            return "cuda"


        return "cpu"


    @staticmethod

    def available():


        return (

            torch.cuda.is_available()

        )