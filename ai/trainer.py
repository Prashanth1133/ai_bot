import os
import gc
import torch
import torch.nn as nn

from torch.utils.data import DataLoader

from torch.cuda.amp import (
    autocast,
    GradScaler,
)


class Trainer:


    #################################################

    def __init__(

        self,
        model,
        dataset,
        save_path="models/trading_transformer.pt",
        batch_size=64,
        lr=1e-4,
        patience=30,

    ):


        #################################################

        self.device = torch.device(

            "cuda"

            if torch.cuda.is_available()

            else

            "cpu"

        )


        #################################################

        print()

        print("="*60)
        print("Using Device :",self.device)
        print("="*60)
        print()


        #################################################

        if torch.cuda.is_available():

            gpu_memory = (

                torch.cuda.get_device_properties(
                    0
                ).total_memory

                /(1024**3)

            )


            if gpu_memory >= 15:

                batch_size = 512


            elif gpu_memory >=10:

                batch_size = 256


            else:

                batch_size = 128


            workers = 2

            pin_memory=True


        else:

            batch_size = 64

            workers=0

            pin_memory=False


        #################################################

        self.model = (

            model.to(

                self.device

            )

        )


        self.save_path = save_path

        self.best_loss = 999999

        self.patience = patience

        self.counter = 0


        #################################################

        self.loader = DataLoader(

            dataset,

            batch_size=batch_size,

            shuffle=True,

            pin_memory=pin_memory,

            num_workers=workers,

            drop_last=False,

        )


        #################################################

        self.optimizer = (

            torch.optim.AdamW(

                self.model.parameters(),

                lr=lr,

                weight_decay=1e-5

            )

        )


        #################################################

        self.scheduler = (

            torch.optim.lr_scheduler.

            ReduceLROnPlateau(

                self.optimizer,

                mode="min",

                factor=0.5,

                patience=5,

            )

        )


        #################################################

        self.scaler = GradScaler()


        #################################################

        self.ce = (

            nn.CrossEntropyLoss()

        )


        self.mse = (

            nn.MSELoss()

        )


        #################################################

        os.makedirs(

            "models/checkpoints",

            exist_ok=True

        )


        #################################################

        self.history=[]


    #################################################

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


    #################################################

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


        torch.save(

            checkpoint,

            "models/checkpoints/latest.pt"

        )


        #################################################


        if loss < self.best_loss:


            self.best_loss = loss


            torch.save(

                checkpoint,

                "models/checkpoints/best.pt"

            )


            print(

                "Best Model Saved."

            )


    #################################################

    def clear_gpu(self):


        gc.collect()


        if torch.cuda.is_available():

            torch.cuda.empty_cache()


    #################################################

    def train(

        self,
        epochs=200

    ):


        self.model.train()


        #################################################

        for epoch in range(epochs):


            total_loss=0

            batch_count=0


            #################################################

            for x,y in self.loader:


                try:


                    #################################

                    x = x.to(

                        self.device,

                        non_blocking=True

                    )


                    #################################

                    if self.has_nan(x):

                        continue


                    #################################

                    skip=False


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

                            skip=True

                            break


                    if skip:

                        continue


                    #################################

                    self.optimizer.zero_grad(

                        set_to_none=True

                    )


                    #################################

                    with autocast(


                        enabled=

                        torch.cuda.is_available()

                    ):


                        outputs = (

                            self.model(

                                x

                            )

                        )


                        #################################

                        loss =0


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


                    #################################

                    if torch.isnan(loss):

                        continue


                    if torch.isinf(loss):

                        continue


                    #################################

                    self.scaler.scale(

                        loss

                    ).backward()


                    #################################

                    torch.nn.utils.clip_grad_norm_(

                        self.model.parameters(),

                        1.0

                    )


                    #################################

                    self.scaler.step(

                        self.optimizer

                    )


                    self.scaler.update()


                    #################################

                    total_loss += (

                        loss.item()

                    )


                    batch_count +=1


                #################################################

                except RuntimeError as error:


                    if "out of memory" in str(error):


                        print(

                            "\nCUDA OOM"

                        )


                        self.clear_gpu()


                        continue


                    raise error


            #################################################

            if batch_count==0:

                continue


            #################################################

            epoch_loss=(

                total_loss

                /

                batch_count

            )


            #################################################

            print(

                f"Epoch "

                f"{epoch+1}/{epochs}"

                f"    Loss = "

                f"{epoch_loss:.6f}"

            )


            #################################################

            self.scheduler.step(

                epoch_loss

            )


            #################################################

            self.history.append(

                epoch_loss

            )


            #################################################

            self.save_checkpoint(

                epoch+1,

                epoch_loss

            )


            #################################################

            if epoch_loss < self.best_loss:

                self.counter=0

            else:

                self.counter +=1


            #################################################

            if self.counter >= self.patience:


                print()

                print(

                    "Early Stopping."

                )

                print()

                break


            #################################################

            self.clear_gpu()


        #################################################

        torch.save(

            self.model.state_dict(),

            self.save_path

        )


        #################################################

        print()

        print("="*60)
        print("MODEL SAVED")
        print(self.save_path)
        print("="*60)
        print()


    #################################################

    def get_device(

        self

    ):

        return self.device