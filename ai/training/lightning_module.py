import lightning as L

from ai.models.losses import TradingLoss


class CryptoLightningModule(

    L.LightningModule

):

    def __init__(

        self,

        model,

        optimizer,

        scheduler,

    ):

        super().__init__()

        self.model = model

        self.loss_fn = TradingLoss()

        self.optimizer_builder = optimizer

        self.scheduler_builder = scheduler

    def forward(

        self,

        tf5,

        tf15,

        tf1h,

        symbol,

    ):

        return self.model(

            tf5,

            tf15,

            tf1h,

            symbol,

        )

    def training_step(

        self,

        batch,

        batch_idx,

    ):

        tf5, tf15, tf1h, symbol, target = batch

        prediction = self(

            tf5,

            tf15,

            tf1h,

            symbol,

        )

        loss = self.loss_fn(

            prediction,

            target,

        )

        self.log(

            "train_loss",

            loss,

            prog_bar=True,

        )

        return loss

    def validation_step(

        self,

        batch,

        batch_idx,

    ):

        tf5, tf15, tf1h, symbol, target = batch

        prediction = self(

            tf5,

            tf15,

            tf1h,

            symbol,

        )

        loss = self.loss_fn(

            prediction,

            target,

        )

        self.log(

            "val_loss",

            loss,

            prog_bar=True,

        )

    def configure_optimizers(self):

        optimizer = self.optimizer_builder(

            self.model,

        )

        scheduler = self.scheduler_builder(

            optimizer,

        )

        return {

            "optimizer": optimizer,

            "lr_scheduler": scheduler,

        }