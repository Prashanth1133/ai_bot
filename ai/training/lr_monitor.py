from lightning.pytorch.callbacks import LearningRateMonitor


def build_lr_monitor():

    return LearningRateMonitor(
        logging_interval="step"
    )