import subprocess

coins = [

    "train_btc.py",
    "train_eth.py",
    "train_doge.py"

]

for coin in coins:

    print(

        f"Running {coin}"

    )

    subprocess.run(

        [

            "python",
            f"training/{coin}"

        ]

    )