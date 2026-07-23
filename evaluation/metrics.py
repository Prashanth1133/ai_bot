import torch


class Metrics:


    @staticmethod
    def direction_accuracy(

        prediction,
        target

    ):


        prediction = torch.argmax(

            prediction,
            dim=-1

        )


        correct = (

            prediction == target

        ).sum().item()


        total = len(

            target

        )


        return (

            correct / total

        )


    @staticmethod
    def reversal_accuracy(

        prediction,
        target

    ):


        prediction = torch.argmax(

            prediction,
            dim=-1

        )


        correct = (

            prediction == target

        ).sum().item()


        total = len(

            target

        )


        return (

            correct / total

        )


    @staticmethod
    def regime_accuracy(

        prediction,
        target

    ):


        prediction = torch.argmax(

            prediction,
            dim=-1

        )


        correct = (

            prediction == target

        ).sum().item()


        total = len(

            target

        )


        return (

            correct / total

        )


    @staticmethod
    def mse(

        prediction,
        target

    ):


        return (

            (

                prediction -

                target

            ) ** 2

        ).mean().item()



    @staticmethod
    def print_metrics(


        direction,

        reversal,

        regime,

        volatility,

        tp,

        sl


    ):


        print("\n")


        print(

            f"Direction Accuracy : "

            f"{direction:.4f}"

        )


        print(

            f"Reversal Accuracy : "

            f"{reversal:.4f}"

        )


        print(

            f"Regime Accuracy : "

            f"{regime:.4f}"

        )


        print(

            f"Volatility Loss : "

            f"{volatility:.8f}"

        )


        print(

            f"Take Profit Loss : "

            f"{tp:.8f}"

        )


        print(

            f"Stop Loss Loss : "

            f"{sl:.8f}"

        )


        print("\n")