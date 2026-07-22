from lightning.pytorch.loggers import TensorBoardLogger


def build_logger():

    return TensorBoardLogger(

        "logs",

        name="crypto_ai"

    )