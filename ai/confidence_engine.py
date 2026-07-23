import torch


class ConfidenceEngine:


    @staticmethod
    def calculate(

        confidence

    ):


        if isinstance(

            confidence,
            torch.Tensor

        ):

            confidence = (

                confidence.item()

            )


        confidence *= 100


        return round(

            confidence,

            2

        )


    @staticmethod
    def approved(

        confidence

    ):


        return confidence >= 85