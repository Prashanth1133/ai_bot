import os
import torch
import torch.nn as nn

from torch.utils.data import DataLoader
from torch.cuda.amp import GradScaler
from torch.cuda.amp import autocast


class Trainer:

    def __init__(

        self,
        model,
        dataset,
        save_path="models/trading_transformer.pt",
        batch_size=64,
        lr=1e-4

    ):

        self.device = torch.device(

            "cuda"

            if torch.cuda.is_available()

            else

            "cpu"

        )

        print("\n")
        print("="*60)
        print("Using Device :",self.device)
        print("="*60)
        print("\n")


        ################################################

        if torch.cuda.is_available():

            batch_size = 256

            workers = 4

            pin_memory = True

        else:

            batch_size = 64

            workers = 0

            pin_memory = False


        ################################################

        self.model = model.to(

            self.device

        )

        self.save_path = save_path


        self.loader = DataLoader(

            dataset,

            batch_size=batch_size,

            shuffle=True,

            num_workers=workers,

            pin_memory=pin_memory,

            drop_last=False

        )


        ################################################

        self.optimizer = torch.optim.AdamW(

            self.model.parameters(),

            lr=lr,

            weight_decay=1e-4

        )


        ################################################

        self.ce = nn.CrossEntropyLoss()

        self.mse = nn.MSELoss()


        ################################################

        self.scaler = GradScaler(

            enabled=torch.cuda.is_available()

        )


    ####################################################

    def train(

        self,
        epochs=20

    ):


        self.model.train()


        for epoch in range(epochs):

            total_loss = 0.0


            ################################################

            for x,y in self.loader:


                x = x.to(

                    self.device,

                    non_blocking=True

                )


                for key in y:

                    y[key] = y[key].to(

                        self.device,

                        non_blocking=True

                    )


                ################################################

                self.optimizer.zero_grad(

                    set_to_none=True

                )


                ################################################

                with autocast(

                    enabled=torch.cuda.is_available()

                ):


                    outputs = self.model(

                        x

                    )


                    loss = 0


                    ################################################

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


                    ################################################

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


                ################################################

                self.scaler.scale(

                    loss

                ).backward()


                ################################################

                self.scaler.unscale_(

                    self.optimizer

                )


                torch.nn.utils.clip_grad_norm_(

                    self.model.parameters(),

                    max_norm=1.0

                )


                ################################################

                self.scaler.step(

                    self.optimizer

                )

                self.scaler.update()


                ################################################

                total_loss += loss.item()


            ################################################

            print(

                f"Epoch "

                f"{epoch+1}/{epochs}"

                f"  Loss = "

                f"{total_loss:.4f}"

            )


        ####################################################

        os.makedirs(

            "models",

            exist_ok=True

        )


        torch.save(

            self.model.state_dict(),

            self.save_path

        )


        ####################################################

        print("\n")
        print("="*60)
        print("MODEL SAVED")
        print(self.save_path)
        print("="*60)
        print("\n")



    ####################################################

    def get_device(self):

        return self.device