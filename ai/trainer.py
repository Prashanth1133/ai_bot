# ai/trainer.py

from __future__ import annotations

import csv
import gc
import json
import os
import random
import time
from pathlib import Path
from typing import Any

import numpy as np
import torch
import torch.nn as nn
from torch.utils.data import DataLoader, Dataset

from ai.losses import MultiTaskLoss


class Trainer:
    """
    Production Multi-Task Transformer Trainer with support for:
    - Lazy dataset streaming (FinalDataset)
    - Chronological pre-split Train / Validation sets (No random_split)
    - Multi-task Huber/CE loss calculations
    - Automatic mixed precision (AMP)
    - Checkpoint recovery & full telemetry logging
    """

    def auto_seed(self, seed: int = 42) -> None:
        random.seed(seed)
        np.random.seed(seed)
        torch.manual_seed(seed)
        if torch.cuda.is_available():
            torch.cuda.manual_seed(seed)
            torch.cuda.manual_seed_all(seed)
            torch.backends.cudnn.deterministic = True
            torch.backends.cudnn.benchmark = False

    def __init__(
        self,
        model: nn.Module,
        dataset: Dataset,
        validation_dataset: Dataset | None = None,
        save_path: str | None = None,
        drive_path: str | None = None,
        production_dir: str | None = None,
        batch_size: int = 256,
        lr: float = 1e-4,
        weight_decay: float = 1e-5,
        max_epochs: int = 100,
        min_epochs: int = 10,
        lr_patience: int = 3,
        lr_factor: float = 0.5,
        early_stop_patience: int = 10,
        minimum_lr: float = 1e-7,
        maximum_lr_reduction: int = 5,
        gradient_clip: float = 1.0,
        checkpoint_interval: int = 10,
        epoch_interval: int = 10,
        validation_split: float = 0.15,
        resume: bool = False,
        seed: int = 42,
        workers: int | None = None,
        pin_memory: bool | None = None,
    ):
        self.auto_seed(seed)
        self.resume = resume
        self.lr = lr
        self.weight_decay = weight_decay
        self.max_epochs = max_epochs
        self.min_epochs = min_epochs
        self.lr_patience = lr_patience
        self.lr_factor = lr_factor
        self.early_stop_patience = early_stop_patience
        self.minimum_lr = minimum_lr
        self.maximum_lr_reduction = maximum_lr_reduction
        self.gradient_clip = gradient_clip
        self.checkpoint_interval = checkpoint_interval
        self.epoch_interval = epoch_interval
        self.validation_split = None

        # ----------------------------------------------------
        # Storage Location Configuration
        # ----------------------------------------------------
        if production_dir is not None:
            self.production_dir = os.path.abspath(production_dir)
        elif drive_path is not None:
            drive_path = os.path.abspath(drive_path)
            self.production_dir = os.path.join(drive_path, "Production", "BTCUSDT", "final_v1")
        else:
            self.production_dir = os.path.abspath("models/Production/BTCUSDT/final_v1")

        os.makedirs(self.production_dir, exist_ok=True)
        os.makedirs(os.path.join(self.production_dir, "Epochs"), exist_ok=True)
        os.makedirs(os.path.join(self.production_dir, "Checkpoints"), exist_ok=True)

        if save_path is None:
            self.save_path = os.path.join(self.production_dir, "final_model.pt")
        else:
            self.save_path = os.path.abspath(save_path)
            os.makedirs(os.path.dirname(self.save_path), exist_ok=True)

        self.best_save_path = os.path.join(self.production_dir, "best_model.pt")

        # ----------------------------------------------------
        # Device & Memory Detection
        # ----------------------------------------------------
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

        if torch.cuda.is_available():
            total_mem_gb = round(
                torch.cuda.get_device_properties(0).total_memory / (1024**3), 2
            )
            # Default batch size if not explicitly configured
            if batch_size is None:
                if total_mem_gb >= 24:
                    batch_size = 256
                elif total_mem_gb >= 12:
                    batch_size = 256
                else:
                    batch_size = 128

            self.workers = workers if workers is not None else 2
            self.pin_memory = pin_memory if pin_memory is not None else True
            self.use_amp = True
        else:
            total_mem_gb = 0.0
            if batch_size is None:
                batch_size = 64
            self.workers = workers if workers is not None else 0
            self.pin_memory = pin_memory if pin_memory is not None else False
            self.use_amp = False

        self.batch_size = batch_size
        self.scaler = torch.amp.GradScaler("cuda", enabled=self.use_amp)

        print("\n" + "=" * 60)
        print(" TRAINING ENGINE INITIALIZED")
        print(f" Device          : {self.device}")
        print(f" Batch Size      : {self.batch_size}")
        print(f" Max Budget      : {self.max_epochs} epochs (Min: {self.min_epochs})")
        print(f" Workers         : {self.workers}")
        print(f" Mixed Precision : {self.use_amp}")
        print(f" Production Dir  : {self.production_dir}")
        print(f" Save Path       : {self.save_path}")
        print("=" * 60 + "\n")

        # ----------------------------------------------------
        # Dataset & Chronological Pre-Split Handling
        # ----------------------------------------------------
        if validation_dataset is None:
            raise ValueError(
                "\n[DATASET ERROR] Chronological validation dataset is required.\n"
                "Random dataset splitting is disabled for production training.\n"
                "Provide the forensic-audited chronological Train and Validation "
                "datasets with the purge gap preserved."
            )

        self.train_dataset = dataset
        self.validation_dataset = validation_dataset

        train_size = len(self.train_dataset)
        validation_size = len(self.validation_dataset)
        total_size = train_size + validation_size

        if train_size <= 0:
            raise ValueError("[DATASET ERROR] Training dataset is empty.")

        if validation_size <= 0:
            raise ValueError("[DATASET ERROR] Validation dataset is empty.")

        print("\n[DATASET] Using pre-split chronological datasets:")
        print(f"  Train samples     : {train_size:,}")
        print(f"  Validation samples: {validation_size:,}")
        print(f"  Combined samples  : {total_size:,}")
        print("  Random split      : DISABLED")
        print("  Leakage protection: ENABLED")

        self.loader = DataLoader(
            self.train_dataset,
            batch_size=self.batch_size,
            shuffle=True,
            pin_memory=self.pin_memory,
            num_workers=self.workers,
            drop_last=False,
        )

        self.validation_loader = DataLoader(
            self.validation_dataset,
            batch_size=self.batch_size,
            shuffle=False,
            pin_memory=self.pin_memory,
            num_workers=self.workers,
            drop_last=False,
        )

        # ----------------------------------------------------
        # Model & Optimization Setup
        # ----------------------------------------------------
        self.original_model = model
        self.model = model.to(self.device)

        self.optimizer = torch.optim.AdamW(
            self.model.parameters(),
            lr=self.lr,
            weight_decay=self.weight_decay,
        )

        self.scheduler = torch.optim.lr_scheduler.ReduceLROnPlateau(
            self.optimizer,
            mode="min",
            factor=self.lr_factor,
            patience=self.lr_patience,
            min_lr=self.minimum_lr,
            threshold=1e-4,
        )

        # Multi-task criterion
        self.criterion = MultiTaskLoss(
            direction_weight=1.00,
            reversal_weight=0.50,
            return_15m_weight=0.25,
            return_1h_weight=0.25,
            return_4h_weight=0.25,
            max_return_1h_weight=0.25,
            min_return_1h_weight=0.25,
            tp_weight=0.50,
            sl_weight=0.50,
        )

        # State tracking
        self.best_loss = float("inf")
        self.best_validation_loss = float("inf")
        self.best_epoch = 0
        self.no_improvement = 0
        self.start_epoch = 0
        self.lr_reduction_count = 0
        self.training_history: list[list[Any]] = []

        # Save metadata
        self.save_dataset_information(total_size, train_size, validation_size)
        self.save_training_configuration()
        self.save_gpu_information()

        if self.resume:
            self.load_checkpoint()

        self.verify_storage()
        self.validate_dataset_contract()

    # ========================================================
    # Internal Utility & Safety Checks
    # ========================================================

    def validate_dataset_contract(self) -> None:
        if len(self.train_dataset) <= 0:
            raise RuntimeError("[DATASET CONTRACT] Empty training dataset.")

        if len(self.validation_dataset) <= 0:
            raise RuntimeError("[DATASET CONTRACT] Empty validation dataset.")

        if len(self.train_dataset) < 1000:
            raise RuntimeError(
                f"[DATASET CONTRACT] Training dataset too small: "
                f"{len(self.train_dataset):,}"
            )

        if len(self.validation_dataset) < 500:
            raise RuntimeError(
                f"[DATASET CONTRACT] Validation dataset too small: "
                f"{len(self.validation_dataset):,}"
            )

        print("\n[DATASET CONTRACT] PASSED")
        print(f"  Train       : {len(self.train_dataset):,}")
        print(f"  Validation  : {len(self.validation_dataset):,}")
        print("  Random split: DISABLED")
        print("  Test data   : NOT USED")

    def has_nan(self, tensor: torch.Tensor) -> bool:
        return torch.isnan(tensor).any() or torch.isinf(tensor).any()

    def gradient_exploded(self) -> bool:
        for p in self.original_model.parameters():
            if p.grad is not None:
                if torch.isnan(p.grad).any() or torch.isinf(p.grad).any():
                    return True
        return False

    def clear_gpu(self) -> None:
        gc.collect()
        if torch.cuda.is_available():
            torch.cuda.empty_cache()
            torch.cuda.ipc_collect()

    def calculate_loss(
        self,
        outputs: dict[str, torch.Tensor],
        targets: dict[str, torch.Tensor],
    ) -> torch.Tensor:
        return self.criterion(outputs, targets)

    # ========================================================
    # Validation Loop
    # ========================================================

    def validate(self) -> tuple[float, dict[str, Any], dict[str, float]]:
        self.model.eval()
        total_loss = 0.0
        batches = 0
        total_components: dict[str, float] = {}

        all_dir_preds = []
        all_dir_targets = []

        with torch.no_grad():
            for batch in self.validation_loader:
                if isinstance(batch, (tuple, list)):
                    x, y = batch[0], batch[1]
                else:
                    x = batch["features"]
                    y = batch

                x = x.to(self.device, non_blocking=True)
                if self.has_nan(x):
                    continue

                for key in y:
                    if torch.is_tensor(y[key]):
                        y[key] = y[key].to(self.device, non_blocking=True)

                with torch.amp.autocast("cuda", enabled=self.use_amp):
                    outputs = self.model(x)
                    loss, components = self.criterion(outputs, y, return_components=True)

                if torch.isnan(loss) or torch.isinf(loss):
                    continue

                total_loss += loss.item()
                for comp_k, comp_v in components.items():
                    total_components[comp_k] = total_components.get(comp_k, 0.0) + comp_v
                batches += 1

                if "direction" in outputs and "direction" in y:
                    preds = torch.argmax(outputs["direction"], dim=-1).cpu().numpy()
                    tgts = y["direction"].cpu().numpy()
                    all_dir_preds.extend(preds)
                    all_dir_targets.extend(tgts)

        self.model.train()
        avg_loss = total_loss / batches if batches > 0 else float("inf")
        avg_components = {k: v / batches for k, v in total_components.items()} if batches > 0 else {}

        metrics_summary: dict[str, Any] = {}
        if all_dir_targets:
            from evaluation.metrics import Metrics
            metrics_summary = Metrics.classification_metrics(
                y_true=all_dir_targets,
                y_pred=all_dir_preds,
                num_classes=3,
                class_names=["SELL", "HOLD", "BUY"],
            )

        return avg_loss, metrics_summary, avg_components

    # ========================================================
    # Checkpointing & Persistence
    # ========================================================

    def save_best_model(self) -> None:
        torch.save(self.original_model.state_dict(), self.best_save_path)
        if hasattr(os, "sync"):
            os.sync()

    def restore_best_model(self) -> None:
        if os.path.exists(self.best_save_path):
            best_weights = torch.load(self.best_save_path, map_location=self.device)
            self.original_model.load_state_dict(best_weights)
            self.model.load_state_dict(best_weights)
            print("\n[INFO] Best model weights restored from best_model.pt.")

    def save_epoch_model(self, epoch: int) -> None:
        path = os.path.join(self.production_dir, "Epochs", f"epoch_{epoch}.pt")
        torch.save(self.original_model.state_dict(), path)
        if hasattr(os, "sync"):
            os.sync()

    def save_optimizer(self) -> None:
        path = os.path.join(self.production_dir, "optimizer.pt")
        torch.save(self.optimizer.state_dict(), path)

    def save_scheduler(self) -> None:
        path = os.path.join(self.production_dir, "scheduler.pt")
        torch.save(self.scheduler.state_dict(), path)

    def save_complete_model(self) -> None:
        path = os.path.join(self.production_dir, "complete_model.pt")
        torch.save(self.original_model, path)

    def save_checkpoint(self, epoch: int) -> None:
        path = os.path.join(self.production_dir, "Checkpoints", f"checkpoint_{epoch}.pt")
        torch.save(self._build_checkpoint_state(epoch), path)
        if hasattr(os, "sync"):
            os.sync()

    def update_latest(self, epoch: int) -> None:
        path = os.path.join(self.production_dir, "Checkpoints", "latest.pt")
        torch.save(self._build_checkpoint_state(epoch), path)
        if hasattr(os, "sync"):
            os.sync()

    def _build_checkpoint_state(self, epoch: int) -> dict[str, Any]:
        return {
            "epoch": epoch,
            "model": self.original_model.state_dict(),
            "optimizer": self.optimizer.state_dict(),
            "scheduler": self.scheduler.state_dict(),
            "scaler": self.scaler.state_dict() if self.use_amp else None,
            "history": self.training_history,
            "best_epoch": self.best_epoch,
            "best_loss": self.best_loss,
            "best_validation_loss": self.best_validation_loss,
            "no_improvement": self.no_improvement,
            "lr_reduction_count": self.lr_reduction_count,
            "training_configuration": {
                "learning_rate": self.lr,
                "batch_size": self.batch_size,
                "workers": self.workers,
                "validation_split": None,
                "split_strategy": "chronological_pre_split_with_purge",
                "max_epochs": self.max_epochs,
                "min_epochs": self.min_epochs,
                "lr_patience": self.lr_patience,
                "lr_factor": self.lr_factor,
                "checkpoint_interval": self.checkpoint_interval,
                "early_stop": self.early_stop_patience,
                "maximum_lr_reduction": self.maximum_lr_reduction,
                "minimum_lr": self.minimum_lr,
                "gradient_clip": self.gradient_clip,
            },
        }

    def load_checkpoint(self) -> None:
        latest = os.path.join(self.production_dir, "Checkpoints", "latest.pt")
        checkpoint = None
        checkpoint_source = None

        if os.path.exists(latest):
            try:
                checkpoint = torch.load(latest, map_location=self.device)
                checkpoint_source = latest
                print(f"[CHECKPOINT] Loaded latest checkpoint: {latest}")
            except Exception as e:
                print(f"[CHECKPOINT] Failed reading latest.pt: {e}")
                checkpoint = None

        if checkpoint is None:
            folder = os.path.join(self.production_dir, "Checkpoints")
            if os.path.exists(folder):
                files = [f for f in os.listdir(folder) if f.startswith("checkpoint_") and f.endswith(".pt")]
                if files:
                    files.sort()
                    chosen = os.path.join(folder, files[-1])
                    checkpoint = torch.load(chosen, map_location=self.device)
                    checkpoint_source = chosen
                    print(f"[CHECKPOINT] Loaded backup checkpoint: {chosen}")

        if checkpoint is None:
            print("[CHECKPOINT] No existing checkpoint found. Starting fresh.")
            return

        self.original_model.load_state_dict(checkpoint["model"])
        self.model.load_state_dict(checkpoint["model"])
        self.optimizer.load_state_dict(checkpoint["optimizer"])
        self.scheduler.load_state_dict(checkpoint["scheduler"])
        if self.use_amp and checkpoint.get("scaler") is not None:
            self.scaler.load_state_dict(checkpoint["scaler"])

        self.start_epoch = checkpoint.get("epoch", 0)
        self.training_history = checkpoint.get("history", [])
        self.best_epoch = checkpoint.get("best_epoch", 0)
        self.best_loss = checkpoint.get("best_loss", float("inf"))
        self.best_validation_loss = checkpoint.get("best_validation_loss", float("inf"))
        self.no_improvement = checkpoint.get("no_improvement", 0)
        self.lr_reduction_count = checkpoint.get("lr_reduction_count", 0)

        current_lr = self.optimizer.param_groups[0]["lr"]
        print("\n" + "=" * 60)
        print(" RESUMING TRAINING FROM CHECKPOINT")
        print(f" Checkpoint Source   : {checkpoint_source}")
        print(f" Resuming From Epoch : {self.start_epoch + 1}")
        print(f" Best Validation Loss: {self.best_validation_loss:.6f} (Epoch {self.best_epoch})")
        print(f" Current LR          : {current_lr:.2e}")
        print(f" LR Reductions       : {self.lr_reduction_count}/{self.maximum_lr_reduction}")
        print(f" No-Improvement Count: {self.no_improvement}/{self.early_stop_patience}")
        print("=" * 60 + "\n")

    # ========================================================
    # Telemetry and Information Logging
    # ========================================================

    def save_history(self) -> None:
        path = os.path.join(self.production_dir, "training_history.csv")
        with open(path, "w", newline="") as file:
            writer = csv.writer(file)
            writer.writerow([
                "Epoch", "Train_Loss", "Val_Loss",
                "Dir_Loss", "Rev_Loss",
                "Ret15m", "Ret1h", "Ret4h",
                "Max1h", "Min1h",
                "TP_Loss", "SL_Loss",
                "LR", "Time_Seconds"
            ])
            writer.writerows(self.training_history)

    def save_training_configuration(self) -> None:
        data = {
            "learning_rate": self.lr,
            "weight_decay": self.weight_decay,
            "batch_size": self.batch_size,
            "workers": self.workers,
            "max_epochs": self.max_epochs,
            "min_epochs": self.min_epochs,
            "lr_patience": self.lr_patience,
            "lr_factor": self.lr_factor,
            "early_stop_patience": self.early_stop_patience,
            "maximum_lr_reduction": self.maximum_lr_reduction,
            "minimum_lr": self.minimum_lr,
            "gradient_clip": self.gradient_clip,
            "checkpoint_interval": self.checkpoint_interval,
            "epoch_interval": self.epoch_interval,
            "split_strategy": "chronological_pre_split_with_purge",
            "random_split": False,
            "test_set_used_for_training": False,
            "seed": 42,
        }

        path = os.path.join(
            self.production_dir,
            "training_configuration.json",
        )

        with open(path, "w") as file:
            json.dump(data, file, indent=4)

    def save_dataset_information(
        self,
        total: int,
        train: int,
        validation: int,
    ) -> None:
        data = {
            "total_train_validation_samples": total,
            "training_samples": train,
            "validation_samples": validation,
            "split_strategy": "chronological_pre_split_with_purge",
            "random_split": False,
            "leakage_protection": True,
            "test_set_used_for_training": False,
        }

        path = os.path.join(
            self.production_dir,
            "dataset_information.json",
        )

        with open(path, "w") as file:
            json.dump(data, file, indent=4)

    def save_gpu_information(self) -> None:
        if torch.cuda.is_available():
            data = {
                "gpu_name": torch.cuda.get_device_name(0),
                "total_memory_gb": round(torch.cuda.get_device_properties(0).total_memory / (1024**3), 2),
                "cuda_version": torch.version.cuda,
            }
        else:
            data = {"gpu_name": "CPU", "total_memory_gb": 0.0, "cuda_version": "N/A"}
        path = os.path.join(self.production_dir, "gpu_information.json")
        with open(path, "w") as file:
            json.dump(data, file, indent=4)

    def save_best_information(self) -> None:
        data = {
            "best_epoch": self.best_epoch,
            "best_validation_loss": self.best_validation_loss,
            "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
        }
        path = os.path.join(self.production_dir, "best_model_information.json")
        with open(path, "w") as file:
            json.dump(data, file, indent=4)

    def verify_storage(self) -> None:
        required = [
            self.production_dir,
            os.path.join(self.production_dir, "Epochs"),
            os.path.join(self.production_dir, "Checkpoints"),
        ]
        for path in required:
            if not os.path.exists(path):
                os.makedirs(path, exist_ok=True)

    def save_everything(self, epoch: int) -> None:
        self.update_latest(epoch)
        torch.save(self.original_model.state_dict(), self.save_path)
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

    # ========================================================
    # Main Training Loop (Convergence & Checkpoint-Driven)
    # ========================================================

    def train(
        self,
        max_epochs: int | None = None,
        min_epochs: int | None = None,
        epochs: int | None = None,
    ) -> None:
        if max_epochs is None and epochs is not None:
            max_epochs = epochs
        if max_epochs is not None:
            self.max_epochs = max_epochs
        if min_epochs is not None:
            self.min_epochs = min_epochs

        self.model.train()
        print(f"\n[TRAIN] Commencing training up to {self.max_epochs} epochs (Min: {self.min_epochs}, Resuming from epoch {self.start_epoch + 1})...\n")

        epoch = self.start_epoch
        last_completed_epoch = epoch

        while True:
            if epoch >= self.max_epochs:
                print("\n" + "=" * 60)
                print(f" MAXIMUM EPOCH BUDGET ({self.max_epochs}) REACHED.")
                print("=" * 60)
                self.restore_best_model()
                break

            epoch += 1
            last_completed_epoch = epoch
            start = time.time()
            total_loss = 0.0
            batches = 0

            for batch in self.loader:
                try:
                    if isinstance(batch, (tuple, list)):
                        x, y = batch[0], batch[1]
                    else:
                        x = batch["features"]
                        y = batch

                    x = x.to(self.device, non_blocking=True)
                    if self.has_nan(x):
                        continue

                    for key in y:
                        if torch.is_tensor(y[key]):
                            y[key] = y[key].to(self.device, non_blocking=True)

                    self.optimizer.zero_grad(set_to_none=True)

                    with torch.amp.autocast("cuda", enabled=self.use_amp):
                        outputs = self.model(x)
                        loss = self.calculate_loss(outputs, y)

                    if torch.isnan(loss) or torch.isinf(loss):
                        continue

                    if self.use_amp:
                        self.scaler.scale(loss).backward()
                        self.scaler.unscale_(self.optimizer)

                        if self.gradient_exploded():
                            print("\n[WARNING] Gradient explosion detected. Skipping batch.")
                            self.optimizer.zero_grad(set_to_none=True)
                            self.scaler.update()
                            continue

                        torch.nn.utils.clip_grad_norm_(self.original_model.parameters(), max_norm=self.gradient_clip)
                        self.scaler.step(self.optimizer)
                        self.scaler.update()
                    else:
                        loss.backward()
                        if self.gradient_exploded():
                            print("\n[WARNING] Gradient explosion detected. Skipping batch.")
                            self.optimizer.zero_grad(set_to_none=True)
                            continue

                        torch.nn.utils.clip_grad_norm_(self.original_model.parameters(), max_norm=self.gradient_clip)
                        self.optimizer.step()

                    total_loss += loss.item()
                    batches += 1

                except Exception as error:
                    print(f"\n[ERROR in batch]: {error}")
                    self.clear_gpu()
                    continue

            if batches == 0:
                print(f"[WARNING] Epoch {epoch}: No valid batches computed.")
                continue

            train_loss = total_loss / batches
            validation_loss, val_metrics, comp_losses = self.validate()

            old_lr = self.optimizer.param_groups[0]["lr"]
            self.scheduler.step(validation_loss)
            new_lr = self.optimizer.param_groups[0]["lr"]

            if new_lr < old_lr:
                self.lr_reduction_count += 1
                print(f"\n>> Learning Rate Reduced ({self.lr_reduction_count}/{self.maximum_lr_reduction}): {old_lr:.2e} -> {new_lr:.2e}")
                print(f">> Restoring best model from Epoch {self.best_epoch} (Loss: {self.best_validation_loss:.6f})")
                self.restore_best_model()
                self.no_improvement = 0

            current_lr = new_lr
            elapsed = round(time.time() - start, 2)

            # Build per-class F1 & Task breakdown strings
            d_loss = comp_losses.get("direction", 0.0)
            r_loss = comp_losses.get("reversal", 0.0)
            ret15 = comp_losses.get("return_15m", 0.0)
            ret1h = comp_losses.get("return_1h", 0.0)
            ret4h = comp_losses.get("return_4h", 0.0)
            mx1h = comp_losses.get("max_return_1h", 0.0)
            mn1h = comp_losses.get("min_return_1h", 0.0)
            tp_l = comp_losses.get("take_profit", 0.0)
            sl_l = comp_losses.get("stop_loss", 0.0)

            comp_str = f" [Dir:{d_loss:.3f} Rev:{r_loss:.3f} Ret:{(ret15+ret1h+ret4h):.3f} Exc:{(mx1h+mn1h):.3f} TP:{tp_l:.3f} SL:{sl_l:.3f}]"

            acc_str = ""
            if val_metrics and "accuracy" in val_metrics:
                acc = val_metrics["accuracy"] * 100
                acc_str = f" | Dir Acc: {acc:.1f}%"

            print(
                f"Epoch {epoch:3d}/{self.max_epochs:3d} | "
                f"Train: {train_loss:.5f} | "
                f"Val: {validation_loss:.5f}{comp_str}{acc_str} | "
                f"LR: {current_lr:.1e} | "
                f"{elapsed}s"
            )

            # Record history
            self.training_history.append([
                epoch, train_loss, validation_loss,
                d_loss, r_loss,
                ret15, ret1h, ret4h,
                mx1h, mn1h,
                tp_l, sl_l,
                current_lr, elapsed
            ])

            # Validation improvement check with minimum threshold (MIN_DELTA)
            MIN_DELTA = 1e-5
            if validation_loss < (self.best_validation_loss - MIN_DELTA):
                self.best_loss = validation_loss
                self.best_validation_loss = validation_loss
                self.best_epoch = epoch
                self.no_improvement = 0
                self.save_best_model()
                self.save_best_information()
            else:
                self.no_improvement += 1

            # Routine checkpoint saving
            self.update_latest(epoch)

            if epoch % 5 == 0:
                self.save_everything(epoch)
                self.clear_gpu()

            if epoch % self.epoch_interval == 0:
                self.save_epoch_model(epoch)

            if epoch % self.checkpoint_interval == 0:
                self.save_checkpoint(epoch)

            # Early stopping condition (honors min_epochs)
            if epoch >= self.min_epochs and self.no_improvement >= self.early_stop_patience:
                current_lr = self.optimizer.param_groups[0]["lr"]
                if current_lr > self.minimum_lr and self.lr_reduction_count < self.maximum_lr_reduction:
                    print(f"\n[EARLY STOP] Validation plateau detected at Epoch {epoch} (Patience {self.no_improvement}/{self.early_stop_patience}).")
                    print("Allowing learning-rate scheduler to step and continue learning.")
                    self.no_improvement = 0
                else:
                    print("\n" + "=" * 60)
                    print(" CONVERGENCE REACHED - EARLY STOPPING")
                    print("=" * 60)
                    print(f" Best Epoch            : {self.best_epoch}")
                    print(f" Best Validation Loss  : {self.best_validation_loss:.6f}")
                    print(f" Final Learning Rate   : {current_lr:.2e}")
                    print(f" Total LR Reductions   : {self.lr_reduction_count}/{self.maximum_lr_reduction}")
                    print("=" * 60)
                    self.restore_best_model()
                    break

        # Final saves
        if last_completed_epoch > 0:
            self.save_everything(last_completed_epoch)
        print("\n" + "=" * 60)
        print(f" TRAINING PIPELINE COMPLETE | BEST EPOCH: {self.best_epoch} (Val Loss: {self.best_validation_loss:.6f})")
        print(f" Model Saved to: {self.save_path}")
        print("=" * 60 + "\n")