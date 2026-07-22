from lightning.pytorch.callbacks import ModelCheckpoint


def build_checkpoint():

    return ModelCheckpoint(

        monitor="val_loss",

        mode="min",

        save_top_k=3,

        filename="crypto-{epoch}-{val_loss:.4f}",

    )