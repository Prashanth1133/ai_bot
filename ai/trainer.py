import os

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

    ):

        #################################################

        self.device = torch.device(

            "cuda"

            if torch.cuda.is_available()

            else

            "cpu"

        )

        #################################################

        print("\n")
        print("="*60)
        print("Using Device :",self.device)
        print("="*60)
        print("\n")

        #################################################

        if torch.cuda.is_available():

            torch.backends.cudnn.benchmark = True

            torch.backends.cuda.matmul.allow_tf32 = True

            torch.backends.cudnn.allow_tf32 = True

        #################################################

        if torch.cuda.is_available():

            batch_size = 512
            workers = 2
            pin_memory = True
            persistent_workers = True
            prefetch_factor = 4

        else:

            batch_size = 64
            workers = 0
            pin_memory = False
            persistent_workers = False
            prefetch_factor = None

        #################################################

        self.model = model.to(

            self.device

        )

        self.save_path = save_path

        #################################################

        if workers > 0:

            self.loader = DataLoader(

                dataset,

                batch_size=batch_size,

                shuffle=True,

                num_workers=workers,

                pin_memory=pin_memory,

                persistent_workers=persistent_workers,

                prefetch_factor=prefetch_factor,

                drop_last=False,

            )

        else:

            self.loader = DataLoader(

                dataset,

                batch_size=batch_size,

                shuffle=True,

                num_workers=workers,

                pin_memory=pin_memory,

                drop_last=False,

            )

        #################################################

        self.optimizer = torch.optim.AdamW(

            self.model.parameters(),

            lr=lr,

            weight_decay=1e-5,

        )

        #################################################

        self.ce = nn.CrossEntropyLoss()

        self.mse = nn.MSELoss()

        #################################################

        self.scaler = torch.amp.GradScaler(

            "cuda",

            enabled=torch.cuda.is_available()

        )

    #################################################

    def has_nan(

        self,
        tensor

    ):

        return (

            torch.isnan(tensor).any()

            or

            torch.isinf(tensor).any()

        )

    #################################################

    def train(

        self,
        epochs=20

    ):

        self.model.train()

        #################################################

        for epoch in range(epochs):

            total_loss = 0.0

            batch_count = 0

            #################################################

            for x,y in self.loader:

                #################################################

                x = x.to(

                    self.device,

                    non_blocking=True

                )

                #################################################

                if self.has_nan(x):

                    continue

                #################################################

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

                #################################################

                self.optimizer.zero_grad(

                    set_to_none=True

                )

                #################################################

                try:

                    with torch.amp.autocast(

                        "cuda",

                        enabled=torch.cuda.is_available()

                    ):

                        outputs = self.model(

                            x

                        )

                        #####################################

                        loss = 0

                        #####################################

                        loss += self.ce(

                            outputs["direction"],

                            y["direction"]

                        )

                        #####################################

                        loss += self.ce(

                            outputs["reversal"],

                            y["reversal"]

                        )

                        #####################################

                        loss += self.ce(

                            outputs["market_regime"],

                            y["market_regime"]

                        )

                        #####################################

                        loss += self.mse(

                            outputs["confidence"].squeeze(),

                            y["confidence"]

                        )

                        #####################################

                        loss += self.mse(

                            outputs["volatility"].squeeze(),

                            y["volatility"]

                        )

                        #####################################

                        loss += self.mse(

                            outputs["take_profit"].squeeze(),

                            y["take_profit"]

                        )

                        #####################################

                        loss += self.mse(

                            outputs["stop_loss"].squeeze(),

                            y["stop_loss"]

                        )


                except Exception as error:

                    print(

                        "\nLoss Error :",error

                    )

                    continue


                #################################################

                if torch.isnan(loss):

                    continue


                if torch.isinf(loss):

                    continue

                #################################################

                self.scaler.scale(

                    loss

                ).backward()

                #################################################

                self.scaler.unscale_(

                    self.optimizer

                )

                #################################################

                torch.nn.utils.clip_grad_norm_(

                    self.model.parameters(),

                    max_norm=1.0

                )

                #################################################

                self.scaler.step(

                    self.optimizer

                )

                #################################################

                self.scaler.update()

                #################################################

                total_loss += loss.item()

                batch_count += 1

            #################################################

            if batch_count == 0:

                print(

                    f"Epoch {epoch+1} Failed."

                )

                continue

            #################################################

            epoch_loss = (

                total_loss

                /

                batch_count

            )

            #################################################

            print(

                f"Epoch {epoch+1}/{epochs}"

                f"    Loss = "

                f"{epoch_loss:.6f}"

            )

            #################################################

            if torch.cuda.is_available():

                torch.cuda.empty_cache()

        #################################################

        os.makedirs(

            "models",

            exist_ok=True

        )

        #################################################

        torch.save(

            self.model.state_dict(),

            self.save_path

        )

        #################################################

        print("\n")
        print("="*60)
        print("MODEL SAVED")
        print(self.save_path)
        print("="*60)
        print("\n")

    #################################################

    def get_device(

        self

    ):

        return self.device