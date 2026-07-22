import torch


class Metrics:

    @staticmethod
    def accuracy(predictions, labels):

        predicted = torch.argmax(

            predictions,

            dim=1

        )

        correct = (

            predicted == labels

        ).sum().item()

        return (

            correct /

            len(labels)

        )

    @staticmethod
    def buy_precision(

        predictions,
        labels

    ):

        predicted = torch.argmax(

            predictions,

            dim=1

        )

        tp = (

            (predicted == 2) &
            (labels == 2)

        ).sum().item()

        fp = (

            (predicted == 2) &
            (labels != 2)

        ).sum().item()

        return tp / max(

            tp + fp,

            1

        )