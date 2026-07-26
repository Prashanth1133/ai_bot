# ai/trainer.py


import os
import gc
import torch
import torch.nn as nn

from torch.utils.data import DataLoader

from torch.amp import (
    autocast,
    GradScaler,
)


class Trainer:


    ############################################################

    def __init__(

        self,
        model,
        dataset,
        save_path="models/trading_transformer.pt",
        batch_size=64,
        lr=1e-4,
        patience=30,
        accumulation_steps=2,

    ):


        ########################################################

        self.device = torch.device(

            "cuda"

            if torch.cuda.is_available()

            else

            "cpu"

        )


        ########################################################

        print()

        print("="*60)
        print("Using Device :",self.device)
        print("="*60)
        print()


        ########################################################

        if torch.cuda.is_available():

            gpu_memory = (

                torch.cuda.get_device_properties(

                    0

                ).total_memory

                /(1024**3)

            )


            print(

                f"GPU Memory : "

                f"{round(gpu_memory,2)} GB"

            )


            ############################################

            if gpu_memory >= 15:

                batch_size = 1024


            elif gpu_memory >= 10:

                batch_size = 512


            else:

                batch_size = 256


            workers = 2

            pin_memory = True


        else:


            batch_size = 64

            workers = 0

            pin_memory = False


        ########################################################

        print(

            f"Batch Size : "

            f"{batch_size}"

        )

        print(

            f"Workers : "

            f"{workers}"

        )

        print(

            f"Gradient Accumulation : "

            f"{accumulation_steps}"

        )

        print()


        ########################################################

        self.model = (

            model.to(

                self.device

            )

        )


        ########################################################

        self.save_path = save_path

        self.best_loss = 999999

        self.counter = 0

        self.patience = patience

        self.accumulation_steps = (

            accumulation_steps

        )


        ########################################################

        self.loader = DataLoader(

            dataset,

            batch_size=batch_size,

            shuffle=True,

            pin_memory=pin_memory,

            num_workers=workers,

            drop_last=False,

            persistent_workers=(

                workers > 0

            ),

        )


        ########################################################

        self.optimizer = (

            torch.optim.AdamW(

                self.model.parameters(),

                lr=lr,

                weight_decay=1e-5,

            )

        )


        ########################################################

        self.scheduler = (

            torch.optim.lr_scheduler.

            ReduceLROnPlateau(

                self.optimizer,

                mode="min",

                factor=0.50,

                patience=5,

            )

        )


        ########################################################

        if torch.cuda.is_available():

            self.scaler = (

                GradScaler(

                    "cuda"

                )

            )

        else:

            self.scaler = None


        ########################################################

        self.ce = (

            nn.CrossEntropyLoss()

        )


        self.mse = (

            nn.MSELoss()

        )


        ########################################################

        os.makedirs(

            "models",

            exist_ok=True

        )


        os.makedirs(

            "models/checkpoints",

            exist_ok=True

        )


        ########################################################

        self.history = []


    ############################################################

    def has_nan(

        self,
        tensor

    ):


        return (


            torch.isnan(

                tensor

            ).any()


            or


            torch.isinf(

                tensor

            ).any()

        )


    ############################################################

    def clear_gpu(

        self

    ):


        gc.collect()


        if torch.cuda.is_available():

            torch.cuda.empty_cache()


    ############################################################

    def save_checkpoint(

        self,
        epoch,
        loss

    ):


        checkpoint = {

            "epoch":epoch,

            "loss":loss,

            "model":

            self.model.state_dict(),

            "optimizer":

            self.optimizer.state_dict(),

        }


        ####################################################

        torch.save(

            checkpoint,

            "models/checkpoints/latest.pt"

        )


        ####################################################

        if loss < self.best_loss:


            self.best_loss = loss


            torch.save(

                checkpoint,

                "models/checkpoints/best.pt"

            )


            print(

                "Best Model Saved."

            )


    ############################################################

    def train(

        self,
        epochs=300

    ):


        self.model.train()


        ####################################################

        for epoch in range(epochs):


            total_loss = 0

            batch_count = 0


            ################################################

            for x,y in self.loader:


                try:


                    ########################################

                    x = (

                        x.to(

                            self.device,

                            non_blocking=True

                        )

                    )


                    ########################################

                    if self.has_nan(x):

                        continue


                    ########################################

                    skip_batch = False


                    for key in y:


                        y[key] = (

                            y[key].to(

                                self.device,

                                non_blocking=True

                            )

                        )


                        if self.has_nan(

                            y[key]

                        ):

                            skip_batch=True

                            break


                    if skip_batch:

                        continue


                    ########################################

                    if (


                        batch_count

                        %

                        self.accumulation_steps


                    ) == 0:


                        self.optimizer.zero_grad(

                            set_to_none=True

                        )


                    ########################################

                    with autocast(

                        device_type=

                        self.device.type,

                        enabled=True,

                    ):


                        outputs = (

                            self.model(

                                x

                            )

                        )


                        ####################################

                        loss = 0


                        ####################################

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


                        ####################################

                        loss += self.mse(

                            outputs["confidence"]

                            .squeeze(),

                            y["confidence"]

                        )


                        loss += self.mse(

                            outputs["volatility"]

                            .squeeze(),

                            y["volatility"]

                        )


                        loss += self.mse(

                            outputs["take_profit"]

                            .squeeze(),

                            y["take_profit"]

                        )


                        loss += self.mse(

                            outputs["stop_loss"]

                            .squeeze(),

                            y["stop_loss"]

                        )


                        ####################################

                        loss = (

                            loss

                            /

                            self.accumulation_steps

                        )


                    ########################################

                    if torch.isnan(loss):

                        continue


                    if torch.isinf(loss):

                        continue


                    ########################################

                    if self.scaler is not None:


                        self.scaler.scale(

                            loss

                        ).backward()


                    else:

                        loss.backward()


                    ########################################

                    torch.nn.utils.clip_grad_norm_(

                        self.model.parameters(),

                        max_norm=1.0,

                    )


                    ########################################

                    if (


                        (batch_count + 1)

                        %

                        self.accumulation_steps


                    ) == 0:


                        if self.scaler is not None:


                            self.scaler.step(

                                self.optimizer

                            )


                            self.scaler.update()


                        else:


                            self.optimizer.step()


                    ########################################

                    total_loss += (

                        loss.item()

                        *

                        self.accumulation_steps

                    )


                    batch_count += 1


                ################################################

                except RuntimeError as error:


                    if (


                        "out of memory"

                        in

                        str(error).lower()


                    ):


                        print(

                            "\nCUDA OOM"

                        )


                        self.clear_gpu()

                        continue


                    raise error


            ####################################################

            if batch_count == 0:

                continue


            ####################################################

            epoch_loss = (

                total_loss

                /

                batch_count

            )


            ####################################################

            print(

                f"Epoch "

                f"{epoch+1}/{epochs}"

                f"     Loss = "

                f"{epoch_loss:.6f}"

            )


            ####################################################

            self.history.append(

                epoch_loss

            )


            ####################################################

            self.scheduler.step(

                epoch_loss

            )


            ####################################################

            self.save_checkpoint(

                epoch+1,

                epoch_loss

            )


            ####################################################

            if epoch_loss < self.best_loss:

                self.counter = 0

            else:

                self.counter +=1


            ####################################################

            if self.counter >= self.patience:


                print()

                print(

                    "EARLY STOPPING ACTIVATED."

                )

                print()

                break


        ########################################################

        torch.save(

            self.model.state_dict(),

            self.save_path

        )


        ########################################################

        print()

        print("="*60)
        print("MODEL SAVED")
        print(self.save_path)
        print("="*60)
        print()


    ############################################################

    def get_device(

        self

    ):

        return self.device