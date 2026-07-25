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
        batch_size=128,
        lr=1e-4,
        accumulation_steps=4,

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

        if torch.cuda.is_available():

            print(

                "GPU :",

                torch.cuda.get_device_name(

                    0

                )

            )

        print("=" * 60)
        print("\n")

        ##################################################

        if torch.cuda.is_available():

            torch.backends.cudnn.benchmark = True

            torch.backends.cuda.matmul.allow_tf32 = True

            torch.backends.cudnn.allow_tf32 = True

            torch.set_float32_matmul_precision(

                "high"

            )

        ##################################################

        if torch.cuda.is_available():

            batch_size = 128

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

        self.accumulation_steps = (

            accumulation_steps

        )

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

            torch.optim.lr_scheduler.ReduceLROnPlateau(

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

        self.use_amp = (

            torch.cuda.is_available()

        )

        self.scaler = torch.amp.GradScaler(

            "cuda",

            enabled=self.use_amp

        )

        ##################################################

        self.best_loss = (

            float("inf")

        )

        self.patience = 10

        self.wait = 0

    ##################################################

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

    ##################################################

    def save_checkpoint(

        self,
        epoch

    ):

        os.makedirs(

            "models/checkpoints",

            exist_ok=True

        )

        torch.save(

            self.model.state_dict(),

            f"models/checkpoints/epoch_{epoch}.pt"

        )

    ##################################################

    def train(

        self,
        epochs=100

    ):

        self.model.train()

        ##################################################

        for epoch in range(epochs):

            total_loss = 0.0

            batch_count = 0

            ##################################################

            self.optimizer.zero_grad(

                set_to_none=True

            )

            ##################################################

            for batch_idx, (

                x,
                y

            ) in enumerate(

                self.loader

            ):

                ##################################################

                x = x.to(

                    self.device,

                    non_blocking=True

                )

                ##################################################

                if self.has_nan(x):

                    continue

                ##################################################

                skip = False

                for key in y:

                    y[key] = y[key].to(

                        self.device,

                        non_blocking=True

                    )

                    if self.has_nan(

                        y[key]

                    ):

                        skip = True
                        break

                if skip:

                    continue

                ##################################################

                with torch.amp.autocast(

                    device_type="cuda",

                    enabled=self.use_amp

                ):

                    outputs = self.model(

                        x

                    )

                    ##################################################

                    loss = (

                        self.ce(

                            outputs["direction"],
                            y["direction"]

                        )

                        +

                        self.ce(

                            outputs["reversal"],
                            y["reversal"]

                        )

                        +

                        self.ce(

                            outputs["market_regime"],
                            y["market_regime"]

                        )

                        +

                        self.mse(

                            outputs["confidence"].squeeze(),
                            y["confidence"]

                        )

                        +

                        self.mse(

                            outputs["volatility"].squeeze(),
                            y["volatility"]

                        )

                        +

                        self.mse(

                            outputs["take_profit"].squeeze(),
                            y["take_profit"]

                        )

                        +

                        self.mse(

                            outputs["stop_loss"].squeeze(),
                            y["stop_loss"]

                        )

                    )

                ##################################################

                loss = (

                    loss /

                    self.accumulation_steps

                )

                ##################################################

                if self.use_amp:

                    self.scaler.scale(

                        loss

                    ).backward()

                else:

                    loss.backward()

                ##################################################

                if (

                    (batch_idx + 1)

                    %

                    self.accumulation_steps

                    == 0

                ):

                    ##################################################

                    if self.use_amp:

                        self.scaler.unscale_(

                            self.optimizer

                        )

                    ##################################################

                    torch.nn.utils.clip_grad_norm_(

                        self.model.parameters(),

                        max_norm=1.0

                    )

                    ##################################################

                    if self.use_amp:

                        self.scaler.step(

                            self.optimizer

                        )

                        self.scaler.update()

                    else:

                        self.optimizer.step()

                    ##################################################

                    self.optimizer.zero_grad(

                        set_to_none=True

                    )

                ##################################################

                total_loss += (

                    loss.item()

                    *

                    self.accumulation_steps

                )

                batch_count += 1

            ##################################################

            epoch_loss = (

                total_loss /

                max(

                    batch_count,
                    1

                )

            )

            ##################################################

            self.scheduler.step(

                epoch_loss

            )

            ##################################################

            gpu_memory = 0

            if torch.cuda.is_available():

                gpu_memory = round(

                    torch.cuda.memory_allocated()

                    /

                    (1024**3),

                    2

                )

            ##################################################

            print(

                f"Epoch "

                f"{epoch+1}/{epochs}"

                f"   Loss={epoch_loss:.6f}"

                f"   GPU={gpu_memory} GB"

            )

            ##################################################

            if (

                epoch_loss

                <

                self.best_loss

            ):

                self.best_loss = (

                    epoch_loss

                )

                self.wait = 0

                os.makedirs(

                    "models",

                    exist_ok=True

                )

                torch.save(

                    self.model.state_dict(),

                    "models/best_model.pt"

                )

            else:

                self.wait += 1

            ##################################################

            if (

                (epoch + 1)

                %

                10

                == 0

            ):

                self.save_checkpoint(

                    epoch + 1

                )

            ##################################################

            if (

                self.wait

                >=

                self.patience

            ):

                print(

                    "\nEarly Stopping Activated.\n"

                )

                break

        ##################################################

        os.makedirs(

            "models",

            exist_ok=True

        )

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

    def get_device(

        self

    ):

        return self.device