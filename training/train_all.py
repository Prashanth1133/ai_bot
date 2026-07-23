import subprocess


COINS = [

    "train_btc",

    "train_eth",

    "train_doge"

]


def train_all():

    for coin in COINS:

        print("\n")

        print(

            f"Starting : {coin}"

        )

        subprocess.run(

            [

                "python",

                "-m",

                f"training.{coin}"

            ],

            check=True

        )

        print(

            f"Completed : {coin}"

        )

        print("\n")


    print(

        "\nAll Training Completed."

    )


if __name__ == "__main__":

    train_all()