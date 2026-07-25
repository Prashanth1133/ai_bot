import os
import torch
import torch.nn as nn

from torch.utils.data import DataLoader

from torch.optim.lr_scheduler import (
    CosineAnnealingLR
)

from torch.cuda.amp import (
    GradScaler,
    autocast,
)


class Trainer:


    def __init__(

        self,
        model,
        dataset,
        save_path="models/trading_transformer.pt",
        batch_size=64,
        lr=1e-4,
        early_stop=15,

    ):


        ################################################

        torch.backends.cudnn.benchmark = True


        ################################################

        self.device = torch.device(

            "cuda"

            if torch.cuda.is_available()

            else

            "cpu"

        )


        ################################################

        if torch.cuda.is_available():

            batch_size = 512

            workers = 4

            pin_memory = True

            persistent_workers = True

            prefetch_factor = 4


        else:

            batch_size = 64

            workers = 0

            pin_memory = False

            persistent_workers = False

            prefetch_factor = None


        ################################################

        print("\n")
        print("="*60)
        print("Using Device :",self.device)
        print("Batch Size   :",batch_size)
        print("Workers      :",workers)
        print("="*60)
        print("\n")


        ################################################

        self.model = model.to(

            self.device

        )


        ################################################

        if torch.cuda.is_available():

            try:

                self.model = torch.compile(

                    self.model

                )

                print(

                    "torch.compile() Enabled"

                )

            except Exception:

                print(

                    "torch.compile() skipped."

                )


        ################################################

        self.save_path = save_path


        ################################################

        if workers > 0:

            self.loader = DataLoader(

                dataset,

                batch_size=batch_size,

                shuffle=True,

                num_workers=workers,

                pin_memory=pin_memory,

                persistent_workers=(
                    persistent_workers
                ),

                prefetch_factor=(
                    prefetch_factor
                ),

                drop_last=False,

            )

        else:

            self.loader = DataLoader(

                dataset,

                batch_size=batch_size,

                shuffle=True,

                num_workers=0,

                pin_memory=False,

                drop_last=False,

            )


        ################################################

        self.optimizer = (

            torch.optim.AdamW(

                self.model.parameters(),

                lr=lr,

                weight_decay=1e-5,

            )

        )


        ################################################

        self.scheduler = (

            CosineAnnealingLR(

                self.optimizer,

                T_max=100,

                eta_min=1e-6,

            )

        )


        ################################################

        self.scaler = (

            GradScaler(

                enabled=torch.cuda.is_available()

            )

        )


        ################################################

        self.ce = nn.CrossEntropyLoss()

        self.mse = nn.MSELoss()


        ################################################

        self.best_loss = 999999999

        self.early_stop = early_stop

        self.wait = 0


    ####################################################


    def save_best_model(

        self,
        loss

    ):


        if loss < self.best_loss:


            self.best_loss = loss

            self.wait = 0


            os.makedirs(

                "models",

                exist_ok=True

            )


            torch.save(

                self.model.state_dict(),

                self.save_path

            )


            print(

                "\nBest Model Saved."

            )


        else:

            self.wait += 1


    ####################################################


    def train(

        self,
        epochs=100

    ):


        ################################################

        self.model.train()


        ################################################

        for epoch in range(epochs):


            total_loss = 0.0

            batch_count = 0


            ################################################

            for x,y in self.loader:


                ############################################

                x = x.to(

                    self.device,

                    non_blocking=True

                )


                ############################################

                for key in y:

                    y[key] = (

                        y[key].to(

                            self.device,

                            non_blocking=True

                        )

                    )


                ############################################

                self.optimizer.zero_grad(

                    set_to_none=True

                )


                ############################################

                with autocast(

                    enabled=torch.cuda.is_available()

                ):


                    outputs = (

                        self.model(

                            x

                        )

                    )


                    ####################################

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

                        outputs[
                            "confidence"
                        ].squeeze(),

                        y[
                            "confidence"
                        ]

                    )


                    loss += self.mse(

                        outputs[
                            "volatility"
                        ].squeeze(),

                        y[
                            "volatility"
                        ]

                    )


                    loss += self.mse(

                        outputs[
                            "take_profit"
                        ].squeeze(),

                        y[
                            "take_profit"
                        ]

                    )


                    loss += self.mse(

                        outputs[
                            "stop_loss"
                        ].squeeze(),

                        y[
                            "stop_loss"
                        ]

                    )


                ############################################

                self.scaler.scale(

                    loss

                ).backward()


                ############################################

                self.scaler.unscale_(

                    self.optimizer

                )


                ############################################

                torch.nn.utils.clip_grad_norm_(

                    self.model.parameters(),

                    max_norm=1.0

                )


                ############################################

                self.scaler.step(

                    self.optimizer

                )


                self.scaler.update()


                ############################################

                total_loss += (

                    loss.item()

                )


                batch_count += 1


            ################################################

            epoch_loss = (

                total_loss

                /

                batch_count

            )


            ################################################

            self.scheduler.step()


            ################################################

            print(

                f"Epoch "

                f"{epoch+1}/{epochs}"

                f"    Loss = "

                f"{epoch_loss:.6f}"

            )


            ################################################

            self.save_best_model(

                epoch_loss

            )


            ################################################

            if self.wait >= self.early_stop:


                print()

                print(

                    "="*60

                )

                print(

                    "EARLY STOPPING"

                )

                print(

                    "="*60

                )

                print()


                break


        ################################################

        print("\n")
        print("="*60)
        print("TRAINING COMPLETED")
        print("BEST LOSS :",self.best_loss)
        print("="*60)
        print("\n")


    ####################################################


    def get_device(

        self

    ):

        return self.device