from lightning.pytorch.callbacks import EarlyStopping


def build_early_stopping():

    return EarlyStopping(

        monitor="val_loss",

        patience=10,

        mode="min",

    )