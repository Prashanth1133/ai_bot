import os
import gc
import torch
import torch.nn as nn

from torch.utils.data import DataLoader


class Trainer:

    def __init__(

        self,
        model,
        dataset,
        save_path="models/trading_transformer.pt",
        batch_size=64,
        lr=1e-4,

        checkpoint_interval=20,
        early_stop_patience=25,
        resume=False,

    ):

        ##################################################

        self.device = torch.device(

            "cuda"

            if torch.cuda.is_available()

            else

            "cpu"

        )

        ##################################################

        print("\n")
        print("=" * 60)
        print("Using Device :", self.device)
        print("=" * 60)
        print("\n")

        ##################################################

        if torch.cuda.is_available():

            batch_size = 512
            workers = 2
            pin_memory = True

        else:

            batch_size = 64
            workers = 0
            pin_memory = False

        ##################################################

        self.model = model.to(

            self.device

        )

        self.save_path = save_path

        self.resume = resume

        ##################################################

        self.loader = DataLoader(

            dataset,

            batch_size=batch_size,

            shuffle=True,

            num_workers=workers,

            pin_memory=pin_memory,

            drop_last=False,

        )

        ##################################################

        self.optimizer = torch.optim.AdamW(

            self.model.parameters(),

            lr=lr,

            weight_decay=1e-5,

        )

        ##################################################

        self.scheduler = (

            torch.optim.lr_scheduler.

            ReduceLROnPlateau(

                self.optimizer,

                mode="min",

                factor=0.5,

                patience=5,

            )

        )

        ##################################################

        self.ce = nn.CrossEntropyLoss()

        self.mse = nn.MSELoss()

        ##################################################

        self.best_loss = float("inf")

        self.no_improvement = 0

        self.early_stop_patience = (

            early_stop_patience

        )

        ##################################################

        self.checkpoint_interval = (

            checkpoint_interval

        )

        self.start_epoch = 0

        ##################################################

        self.history = {

            "loss":[]

        }

        ##################################################

        self.scaler = (

            torch.cuda.amp.GradScaler(

                enabled=torch.cuda.is_available()

            )

        )

        ##################################################

        os.makedirs(

            "models",

            exist_ok=True

        )

        os.makedirs(

            "models/checkpoints",

            exist_ok=True

        )

        ##################################################

        if self.resume:

            self.load_checkpoint()

    ##################################################

    def clear_gpu(

        self

    ):

        gc.collect()

        if torch.cuda.is_available():

            torch.cuda.empty_cache()

    ##################################################

    def has_nan(

        self,
        tensor

    ):

        return (

            torch.isnan(tensor).any()

            or

            torch.isinf(tensor).any()

        )

    ##################################################

    def save_checkpoint(

        self,
        epoch

    ):

        path = (

            f"models/checkpoints/"
            f"checkpoint_epoch_"
            f"{epoch}.pt"

        )

        torch.save(

            {

                "epoch":epoch,

                "model":

                self.model.state_dict(),

                "optimizer":

                self.optimizer.state_dict(),

                "scheduler":

                self.scheduler.state_dict(),

                "best_loss":

                self.best_loss,

                "history":

                self.history,

            },

            path

        )

        print(

            f"\nCheckpoint Saved :"

            f"\n{path}"

        )

    ##################################################

    def load_checkpoint(

        self

    ):

        path = (

            "models/checkpoints/"
            "latest.pt"

        )

        if not os.path.exists(

            path

        ):

            return


        checkpoint = torch.load(

            path,

            map_location=self.device,

        )


        self.model.load_state_dict(

            checkpoint["model"]

        )


        self.optimizer.load_state_dict(

            checkpoint["optimizer"]

        )


        self.scheduler.load_state_dict(

            checkpoint["scheduler"]

        )


        self.best_loss = (

            checkpoint["best_loss"]

        )


        self.start_epoch = (

            checkpoint["epoch"]

        )


        self.history = (

            checkpoint.get(

                "history",

                {"loss":[]}

            )

        )


        print()

        print("="*60)

        print(

            "Resuming From Epoch :",

            self.start_epoch

        )

        print("="*60)

        print()

    ##################################################

    def update_latest(

        self,
        epoch

    ):

        path = (

            "models/checkpoints/"
            "latest.pt"

        )

        torch.save(

            {

                "epoch":epoch,

                "model":

                self.model.state_dict(),

                "optimizer":

                self.optimizer.state_dict(),

                "scheduler":

                self.scheduler.state_dict(),

                "best_loss":

                self.best_loss,

                "history":

                self.history,

            },

            path

        )

    ##################################################

    def train(

        self,
        epochs=20

    ):

        self.model.train()

        ##################################################

        for epoch in range(

            self.start_epoch,
            epochs

        ):

            total_loss = 0.0

            batch_count = 0

            ##################################################

            for x,y in self.loader:

                ##################################################

                try:

                    x = x.to(

                        self.device,

                        non_blocking=True

                    )

                except RuntimeError:

                    continue

                ##################################################

                if self.has_nan(x):

                    continue

                ##################################################

                skip_batch = False

                for key in y:

                    y[key] = y[key].to(

                        self.device,

                        non_blocking=True

                    )

                    if self.has_nan(

                        y[key]

                    ):

                        skip_batch = True
                        break

                if skip_batch:

                    continue

                ##################################################

                self.optimizer.zero_grad(

                    set_to_none=True

                )

                ##################################################

                try:

                    with torch.cuda.amp.autocast(

                        enabled=torch.cuda.is_available()

                    ):

                        outputs = self.model(

                            x

                        )

                        ######################################

                        loss = 0

                        loss += self.ce(

                            outputs["direction"],

                            y["direction"]

                        )

                        loss += self.ce(

                            outputs["reversal"],

                            y["reversal"]

                        )

                        loss += self.ce(

                            outputs["market_regime"],

                            y["market_regime"]

                        )

                        loss += self.mse(

                            outputs["confidence"].squeeze(),

                            y["confidence"]

                        )

                        loss += self.mse(

                            outputs["volatility"].squeeze(),

                            y["volatility"]

                        )

                        loss += self.mse(

                            outputs["take_profit"].squeeze(),

                            y["take_profit"]

                        )

                        loss += self.mse(

                            outputs["stop_loss"].squeeze(),

                            y["stop_loss"]

                        )

                except RuntimeError as error:

                    if "out of memory" in str(error):

                        print(

                            "\nCUDA OOM -> Batch Skipped"

                        )

                        self.clear_gpu()

                        continue

                    continue

                ##################################################

                if torch.isnan(loss):

                    continue

                if torch.isinf(loss):

                    continue

                ##################################################

                try:

                    self.scaler.scale(

                        loss

                    ).backward()

                except RuntimeError:

                    self.clear_gpu()

                    continue

                ##################################################

                torch.nn.utils.clip_grad_norm_(

                    self.model.parameters(),

                    max_norm=1.0

                )

                ##################################################

                self.scaler.step(

                    self.optimizer

                )

                self.scaler.update()

                ##################################################

                total_loss += (

                    loss.item()

                )

                batch_count += 1

            ##################################################

            if batch_count == 0:

                print(

                    f"Epoch "

                    f"{epoch+1} Failed."

                )

                continue

            ##################################################

            epoch_loss = (

                total_loss

                /

                batch_count

            )

            ##################################################

            self.history["loss"].append(

                epoch_loss

            )

            ##################################################

            print(

                f"Epoch "

                f"{epoch+1}/{epochs}"

                f"    Loss = "

                f"{epoch_loss:.6f}"

            )

            ##################################################

            self.scheduler.step(

                epoch_loss

            )

            ##################################################

            if epoch_loss < self.best_loss:

                self.best_loss = (

                    epoch_loss

                )

                self.no_improvement = 0

            else:

                self.no_improvement += 1

            ##################################################

            if (

                (epoch+1)

                %

                self.checkpoint_interval

                == 0

            ):

                self.save_checkpoint(

                    epoch+1

                )

                self.update_latest(

                    epoch+1

                )

            ##################################################

            if (

                self.no_improvement

                >=

                self.early_stop_patience

            ):

                print()

                print("="*60)
                print(
                    "EARLY STOPPING ACTIVATED"
                )
                print("="*60)
                print()

                break

            ##################################################

            self.clear_gpu()

        ##################################################

        torch.save(

            self.model.state_dict(),

            self.save_path

        )

        ##################################################

        print("\n")
        print("=" * 60)
        print("MODEL SAVED")
        print(self.save_path)
        print("=" * 60)
        print("\n")

    ##################################################

    def get_history(

        self

    ):

        return self.history

    ##################################################

    def get_device(

        self

    ):

        return self.device