import lightning as L

from ai.training.logger import build_logger
from ai.training.checkpoint import build_checkpoint
from ai.training.early_stopping import build_early_stopping

# NEW
from ai.training.lr_monitor import build_lr_monitor
from ai.training.progress_bar import build_progress_bar


def build_trainer(config):

    callbacks = [

        build_checkpoint(),

        build_early_stopping(),

        build_lr_monitor(),

        build_progress_bar(),

    ]

    trainer = L.Trainer(

        ###################################################
        # Training
        ###################################################

        max_epochs=config.epochs,

        accelerator="auto",

        devices=1,

        precision="16-mixed",

        ###################################################
        # Performance
        ###################################################

        gradient_clip_val=config.gradient_clip,

        accumulate_grad_batches=getattr(
            config,
            "accumulate_grad_batches",
            1,
        ),

        ###################################################
        # Logging
        ###################################################

        logger=build_logger(),

        callbacks=callbacks,

        log_every_n_steps=20,

        ###################################################
        # Validation
        ###################################################

        check_val_every_n_epoch=1,

        ###################################################
        # Deterministic
        ###################################################

        deterministic=False,

        benchmark=True,

    )

    return trainer