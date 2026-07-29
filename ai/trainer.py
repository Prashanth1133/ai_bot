# ai/trainer.py

import os
import gc
import csv
import json
import time
import random
import numpy as np
import torch
import torch.nn as nn

from torch.utils.data import DataLoader
from torch.utils.data import random_split


class Trainer:

    def auto_seed(

        self,

        seed=42

    ):

        random.seed(
            seed
        )

        np.random.seed(
            seed
        )

        torch.manual_seed(
            seed
        )

        if torch.cuda.is_available():

            torch.cuda.manual_seed(
                seed
            )

            torch.cuda.manual_seed_all(
                seed
            )

            torch.backends.cudnn.deterministic = True

    ####################################################

    def __init__(

        self,

        model,

        dataset,

        save_path="models/Production/production_v1.pt",

        batch_size=64,

        lr=1e-4,

        weight_decay=1e-5,

        checkpoint_interval=50,

        epoch_interval=10,

        early_stop_patience=12,

        validation_split=0.10,

        resume=False,

        drive_path=None,

        seed=42,

    ):

        ####################################################

        self.auto_seed(
            seed
        )

        self.resume = resume

        self.lr = lr

        self.weight_decay = weight_decay

        self.validation_split = validation_split

        self.checkpoint_interval = checkpoint_interval

        self.epoch_interval = epoch_interval

        self.early_stop_patience = early_stop_patience

        self.drive_path = drive_path

        ####################################################

        ####################################################
        # STORAGE LOCATION
        ####################################################

        if drive_path is None:

            raise ValueError(
                """
                drive_path is required.
                Training cannot continue without Google Drive path.
                """
            )

        drive_path = os.path.abspath(
            drive_path
        )

        if not os.path.exists(drive_path):

            raise FileNotFoundError(
                f"""
                Drive path not found:

                {drive_path}

                Check Google Drive mount.
                """
            )

        self.production_dir = os.path.join(
            drive_path,
            "Production"
        )

        print(
            "Saving all training files to:"
        )

        print(
            self.production_dir
        )

        ####################################################

        if (

            save_path is None

            or

            save_path == "models/Production/production_v1.pt"

        ):

            self.save_path = os.path.join(

                self.production_dir,

                "production_v1.pt"

            )

        else:

            self.save_path = save_path

        ####################################################

        self.device = torch.device(

            "cuda"

            if torch.cuda.is_available()

            else

            "cpu"

        )

        ####################################################

        if torch.cuda.is_available():

            total_memory = round(

                torch.cuda.get_device_properties(
                    0
                ).total_memory / (1024 ** 3),

                2

            )

            if total_memory >= 14:

                batch_size = 512

          
            elif total_memory>=8:

                batch_size=256

            else:

                batch_size = 64

            workers = 2

            pin_memory = True

        else:

            total_memory = 0

            batch_size = 64

            workers = 0

            pin_memory = False

        ####################################################

        self.batch_size = batch_size

        self.workers = workers

        self.pin_memory = pin_memory

        ####################################################

        print("\n")
        print("=" * 60)
        print("Using Device :", self.device)
        print("Batch Size :", batch_size)
        print("Production Dir :", self.production_dir)
        print("=" * 60)
        print("\n")

        ####################################################

        os.makedirs(

            self.production_dir,

            exist_ok=True

        )

        os.makedirs(

            os.path.join(

                self.production_dir,

                "Epochs"

            ),

            exist_ok=True

        )

        os.makedirs(

            os.path.join(

                self.production_dir,

                "Checkpoints"

            ),

            exist_ok=True

        )

        ####################################################

        total_size = len(dataset)

        validation_size = int(

            total_size *

            validation_split

        )

        train_size = (

            total_size -

            validation_size

        )

        ####################################################

        generator = torch.Generator()

        generator.manual_seed(

            seed

        )

        self.train_dataset, self.validation_dataset = (

            random_split(

                dataset,

                [

                    train_size,
                    validation_size

                ],

                generator=generator

            )

        )

        ####################################################

        self.loader = DataLoader(

            self.train_dataset,

            batch_size=batch_size,

            shuffle=True,

            pin_memory=pin_memory,

            num_workers=workers,

            drop_last=False,

        )

        ####################################################

        self.validation_loader = DataLoader(

            self.validation_dataset,

            batch_size=batch_size,

            shuffle=False,

            pin_memory=pin_memory,

            num_workers=workers,

            drop_last=False,

        )

        ####################################################

        self.original_model = model

        self.model = model.to(

            self.device

        )

        ####################################################

        if (

            torch.cuda.is_available()

            and

            hasattr(

                torch,

                "compile"

            )

        ):

            try:

                self.model = (

                    torch.compile(

                        self.model

                    )

                )

                print(

                    "Model Compiled."

                )

            except Exception:

                pass

        ####################################################

        self.optimizer = torch.optim.AdamW(

            self.model.parameters(),

            lr=lr,

            weight_decay=weight_decay,

        )

        ####################################################

        self.scheduler = (

            torch.optim.lr_scheduler.
            ReduceLROnPlateau(

                self.optimizer,

                mode="min",

                factor=0.50,

                patience=5,

            )

        )

        ####################################################

        self.ce = nn.CrossEntropyLoss()

        self.mse = nn.MSELoss()

        ####################################################

        self.best_loss = float(

            "inf"

        )

        self.no_improvement = 0

        self.start_epoch = 0

        ####################################################

        self.training_history = []

        ####################################################

        self.best_epoch = 0

        self.best_validation_loss = float(

            "inf"

        )

        ####################################################

        self.save_dataset_information(

            total_size,

            train_size,

            validation_size

        )

        self.save_training_configuration()

        self.save_gpu_information()

        ####################################################

        if self.resume:

            self.load_checkpoint()

        self.verify_storage()

    ####################################################

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

    ####################################################

    def gradient_exploded(

        self

    ):

        for parameter in (

            self.original_model.parameters()

        ):

            if parameter.grad is None:

                continue

            if torch.isnan(

                parameter.grad

            ).any():

                return True

            if torch.isinf(

                parameter.grad

            ).any():

                return True

        return False

    ####################################################

    def clear_gpu(

        self

    ):

        gc.collect()

        if torch.cuda.is_available():

            torch.cuda.empty_cache()

            torch.cuda.ipc_collect()

    ####################################################

    def calculate_loss(

        self,
        outputs,
        y

    ):

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

        return loss

    ####################################################

    def validate(

        self

    ):

        self.model.eval()

        total_loss = 0

        batches = 0

        with torch.no_grad():

            for x, y in self.validation_loader:

                x = x.to(self.device)

                if self.has_nan(x):

                    continue

                skip = False

                for key in y:

                    y[key] = y[key].to(

                        self.device

                    )

                    if self.has_nan(

                        y[key]

                    ):

                        skip = True

                        break

                if skip:

                    continue

                outputs = self.model(x)

                loss = self.calculate_loss(

                    outputs,
                    y

                )

                total_loss += (

                    loss.item()

                )

                batches += 1

        self.model.train()

        if batches == 0:

            return 0

        return (

            total_loss /

            batches

        )

    ####################################################

    def save_best_model(

        self

    ):

        path = os.path.join(

            self.production_dir,

            "best_model.pt"

        )

        torch.save(

            self.original_model.state_dict(),

            path

        )

        if hasattr(os, "sync"):

            os.sync()

    ####################################################

    def save_epoch_model(

        self,

        epoch

    ):

        path = os.path.join(

            self.production_dir,

            "Epochs",

            f"epoch_{epoch}.pt"

        )

        torch.save(

            self.original_model.state_dict(),

            path

        )

        if hasattr(os, "sync"):

            os.sync()

    ####################################################

    def save_optimizer(

        self

    ):

        path = os.path.join(

            self.production_dir,

            "optimizer.pt"

        )

        torch.save(

            self.optimizer.state_dict(),

            path

        )

        if hasattr(os, "sync"):

            os.sync()

    ####################################################

    def save_scheduler(

        self

    ):

        path = os.path.join(

            self.production_dir,

            "scheduler.pt"

        )

        torch.save(

            self.scheduler.state_dict(),

            path

        )

        if hasattr(os, "sync"):

            os.sync()

    ####################################################

    def save_complete_model(

        self

    ):

        path = os.path.join(

            self.production_dir,

            "complete_model.pt"

        )

        torch.save(

            self.original_model,

            path

        )

        if hasattr(os, "sync"):

            os.sync()

    ####################################################

    def save_checkpoint(

        self,

        epoch

    ):

        path = os.path.join(

            self.production_dir,

            "Checkpoints",

            f"checkpoint_{epoch}.pt"

        )

        torch.save(

            {

                "epoch": epoch,

                "model":

                self.original_model.state_dict(),

                "optimizer":

                self.optimizer.state_dict(),

                "scheduler":

                self.scheduler.state_dict(),

                "history":

                self.training_history,

                "best_epoch":

                self.best_epoch,

                "best_loss":

                self.best_loss,

                "best_validation_loss":

                self.best_validation_loss,

                "no_improvement":

                self.no_improvement,

                "training_configuration": {

                    "learning_rate": self.lr,

                    "batch_size": self.batch_size,

                    "workers": self.workers,

                    "validation_split": self.validation_split,

                    "checkpoint_interval": self.checkpoint_interval,

                    "early_stop": self.early_stop_patience,

                }

            },

            path

        )

        if hasattr(os, "sync"):

            os.sync()

    ####################################################

    def update_latest(

        self,

        epoch

    ):

        path = os.path.join(

            self.production_dir,

            "Checkpoints",

            "latest.pt"

        )

        torch.save(

            {

                "epoch": epoch,

                "model":

                self.original_model.state_dict(),

                "optimizer":

                self.optimizer.state_dict(),

                "scheduler":

                self.scheduler.state_dict(),

                "history":

                self.training_history,

                "best_epoch":

                self.best_epoch,

                "best_loss":

                self.best_loss,

                "best_validation_loss":

                self.best_validation_loss,

                "no_improvement":

                self.no_improvement,

                "training_configuration": {

                    "learning_rate": self.lr,

                    "batch_size": self.batch_size,

                    "workers": self.workers,

                    "validation_split": self.validation_split,

                    "checkpoint_interval": self.checkpoint_interval,

                    "early_stop": self.early_stop_patience,

                }

            },

            path

        )

        if hasattr(os, "sync"):

            os.sync()

    ####################################################

    def load_checkpoint(

        self

    ):

        latest = os.path.join(

            self.production_dir,

            "Checkpoints",

            "latest.pt"

        )

        checkpoint = None

        if os.path.exists(latest):

            try:

                checkpoint = torch.load(

                    latest,

                    map_location=self.device

                )

            except Exception:

                checkpoint = None

        if checkpoint is None:

            folder = os.path.join(

                self.production_dir,

                "Checkpoints"

            )

            files = []

            if os.path.exists(folder):

                for file in os.listdir(folder):

                    if file.startswith("checkpoint_") and file.endswith(".pt"):

                        files.append(file)

            if len(files) == 0:

                print(

                    "No checkpoint found."

                )

                return

            files.sort(

                key=lambda x: int(

                    x.split("_")[1].replace(".pt", "")

                )

            )

            latest_file = files[-1]

            latest = os.path.join(

                folder,

                latest_file

            )

            try:

                checkpoint = torch.load(

                    latest,

                    map_location=self.device

                )

            except Exception as error:

                print(

                    f"Failed to load checkpoint {latest}: {error}"

                )

                return

        print("\n" + "=" * 60)

        print(

            "RESUMING TRAINING FROM CHECKPOINT:",

            latest

        )

        self.original_model.load_state_dict(

            checkpoint["model"]

        )

        if "optimizer" in checkpoint:

            self.optimizer.load_state_dict(

                checkpoint["optimizer"]

            )

        if "scheduler" in checkpoint:

            self.scheduler.load_state_dict(

                checkpoint["scheduler"]

            )

        if "history" in checkpoint:

            self.training_history = checkpoint["history"]

        if "best_epoch" in checkpoint:

            self.best_epoch = checkpoint["best_epoch"]

        if "best_loss" in checkpoint:

            self.best_loss = checkpoint["best_loss"]

        if "best_validation_loss" in checkpoint:

            self.best_validation_loss = checkpoint["best_validation_loss"]

        if "no_improvement" in checkpoint:

            self.no_improvement = checkpoint["no_improvement"]

        self.start_epoch = checkpoint.get("epoch", 0)

        print(

            f"Resuming from epoch: {self.start_epoch + 1}"

        )

        print(

            "Best validation loss restored:",

            self.best_validation_loss

        )

        print("=" * 60 + "\n")

    ####################################################

    def save_history(

        self

    ):

        path1 = os.path.join(

            self.production_dir,

            "training_history.csv"

        )

        path2 = os.path.join(

            self.production_dir,

            "training.csv"

        )

        for path in [path1, path2]:

            with open(

                path,

                "w",

                newline=""

            ) as file:

                writer = csv.writer(

                    file

                )

                writer.writerow(

                    [

                        "Epoch",

                        "Train Loss",

                        "Validation Loss",

                        "Learning Rate",

                        "Time"

                    ]

                )

                writer.writerows(

                    self.training_history

                )

        if hasattr(os, "sync"):

            os.sync()

    ####################################################

    def save_best_information(

        self

    ):

        data = {

            "best_epoch":

            self.best_epoch,

            "best_validation_loss":

            self.best_validation_loss,

            "device":

            str(

                self.device

            ),

            "batch_size":

            self.batch_size,

            "learning_rate":

            self.lr,

        }

        path = os.path.join(

            self.production_dir,

            "best_model_information.json"

        )

        with open(

            path,

            "w"

        ) as file:

            json.dump(

                data,

                file,

                indent=4

            )

        if hasattr(os, "sync"):

            os.sync()

    ####################################################

    def save_gpu_information(

        self

    ):

        data = {

            "device":

            str(self.device),

        }

        if torch.cuda.is_available():

            data["gpu_name"] = (

                torch.cuda.get_device_name(

                    0

                )

            )

            data["gpu_memory"] = (

                round(

                    torch.cuda.

                    get_device_properties(

                        0

                    ).total_memory

                    /

                    1024**3,

                    2

                )

            )

        path = os.path.join(

            self.production_dir,

            "gpu_information.json"

        )

        with open(

            path,

            "w"

        ) as file:

            json.dump(

                data,

                file,

                indent=4

            )

        if hasattr(os, "sync"):

            os.sync()

    ####################################################

    def save_training_configuration(

        self

    ):

        data = {

            "learning_rate": self.lr,

            "batch_size": self.batch_size,

            "workers": self.workers,

            "validation_split": self.validation_split,

            "checkpoint_interval": self.checkpoint_interval,

            "epoch_interval": self.epoch_interval,

            "early_stop": self.early_stop_patience,

            "drive_path": self.drive_path,

        }

        path = os.path.join(

            self.production_dir,

            "training_configuration.json"

        )

        with open(

            path,

            "w"

        ) as file:

            json.dump(

                data,

                file,

                indent=4

            )

        if hasattr(os, "sync"):

            os.sync()

    ####################################################

    def save_dataset_information(

        self,

        total,

        train,

        validation

    ):

        data = {

            "total_samples": total,

            "training": train,

            "validation": validation,

        }

        path = os.path.join(

            self.production_dir,

            "dataset_information.json"

        )

        with open(

            path,

            "w"

        ) as file:

            json.dump(

                data,

                file,

                indent=4

            )

        if hasattr(os, "sync"):

            os.sync()

    ####################################################

    def verify_storage(

        self

    ):

        required = [

            self.production_dir,

            os.path.join(

                self.production_dir,

                "Epochs"

            ),

            os.path.join(

                self.production_dir,

                "Checkpoints"

            )

        ]

        for path in required:

            if os.path.exists(path):

                print(

                    "FOUND:",

                    path

                )

            else:

                print(

                    "MISSING:",

                    path

                )

    ####################################################

    def save_everything(

        self,

        epoch

    ):

        self.update_latest(

            epoch

        )

        torch.save(

            self.original_model.state_dict(),

            self.save_path

        )

        self.save_history()

        self.save_optimizer()

        self.save_scheduler()

        self.save_best_information()

        self.save_training_configuration()

        self.save_gpu_information()

        if epoch % 5 == 0:

            self.save_complete_model()

        if hasattr(os, "sync"):

            os.sync()

    ####################################################

    def train(

        self,

        epochs=200

    ):

        self.model.train()

        for epoch in range(

            self.start_epoch,

            epochs

        ):

            start = time.time()

            total_loss = 0

            batches = 0

            for x, y in self.loader:

                try:

                    x = x.to(

                        self.device,

                        non_blocking=True

                    )

                    for key in y:

                        y[key] = y[key].to(

                            self.device,

                            non_blocking=True

                        )

                    if self.has_nan(x):

                        continue

                    outputs = self.model(x)

                    loss = self.calculate_loss(

                        outputs,

                        y

                    )

                    if (

                        torch.isnan(loss)

                        or

                        torch.isinf(loss)

                    ):

                        continue

                    self.optimizer.zero_grad(

                        set_to_none=True

                    )

                    loss.backward()

                    if self.gradient_exploded():

                        print(

                            "Gradient Explosion Detected."

                        )

                        self.optimizer.zero_grad(

                            set_to_none=True

                        )

                        continue

                    torch.nn.utils.clip_grad_norm_(

                        self.original_model.parameters(),

                        max_norm=1.0

                    )

                    self.optimizer.step()

                    total_loss += (

                        loss.item()

                    )

                    batches += 1

                except Exception as error:

                    print(

                        "\nERROR :",

                        error

                    )

                    self.clear_gpu()

                    continue

            if batches == 0:

                continue

            train_loss = (

                total_loss /

                batches

            )

            validation_loss = (

                self.validate()

            )

            self.scheduler.step(

                validation_loss

            )

            current_lr = (

                self.optimizer.
                param_groups[0]["lr"]

            )

            print(

                f"Epoch "

                f"{epoch+1}/{epochs}"

                f"    Loss={train_loss:.6f}"

                f"    Val={validation_loss:.6f}"

                f"    LR={current_lr:.8f}"

            )

            if validation_loss < self.best_loss:

                self.best_loss = (

                    validation_loss

                )

                self.best_validation_loss = (

                    validation_loss

                )

                self.best_epoch = (

                    epoch + 1

                )

                self.no_improvement = 0

                self.save_best_model()

                self.save_best_information()

            else:

                self.no_improvement += 1

            elapsed = round(

                time.time() - start,

                2

            )

            self.training_history.append(

                [

                    epoch + 1,

                    train_loss,

                    validation_loss,

                    current_lr,

                    elapsed

                ]

            )

            ##################################################
            # Save latest every epoch
            ##################################################

            self.update_latest(

                epoch + 1

            )

            ##################################################
            # Save everything every 5 epochs
            ##################################################

            if (

                (epoch + 1)

                %

                5

                == 0

            ):

                self.save_everything(

                    epoch + 1

                )

            ##################################################
            # Save epoch model every 10 epochs
            ##################################################

            if (

                (epoch + 1)

                %

                self.epoch_interval

                == 0

            ):

                self.save_epoch_model(

                    epoch + 1

                )

            ##################################################
            # Save backup checkpoint every 50 epochs
            ##################################################

            if (

                (epoch + 1)

                %

                self.checkpoint_interval

                == 0

            ):

                self.save_checkpoint(

                    epoch + 1

                )

            ##################################################

            if (epoch + 1) % 5 == 0:

                self.clear_gpu()

            if (

                self.no_improvement

                >=

                self.early_stop_patience

            ):

                print(

                    "\nEARLY STOPPING.\n"

                )

                break

        ################################################

        torch.save(

            self.original_model.state_dict(),

            self.save_path

        )

        self.save_complete_model()

        self.save_optimizer()

        self.save_scheduler()

        self.save_history()

        self.save_best_information()

        self.save_gpu_information()

        self.save_training_configuration()

        ################################################

        print("\n")

        print("=" * 60)

        print("FINAL MODEL SAVED")

        print(

            "BEST MODEL :",

            self.best_epoch

        )

        print(

            "BEST VALIDATION LOSS :",

            round(

                self.best_validation_loss,

                6

            )

        )

        print(self.save_path)

        print("=" * 60)

        print("\n")