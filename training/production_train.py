from __future__ import annotations

import os
from pathlib import Path

from ai.model import TradingTransformer
from ai.trainer import Trainer
from dataset.final_dataset_loader import FinalDataset
from training.production_checkpoint import ProductionCheckpoint


class ProductionTrain:
    """
    Production training orchestrator for the 400-feature / 128-sequence
    multi-task institutional transformer model using FinalDataset.
    """

    def train(
        self,
        path: str = "dataset/final_unified_dataset.pt",
        save_path: str = "/content/drive/MyDrive/CryptoVisionAI/Production/BTCUSDT/final_v1/final_model.pt",
        drive_path: str = "/content/drive/MyDrive/CryptoVisionAI",
        max_epochs: int = 100,
        min_epochs: int = 10,
        batch_size: int = 256,
        learning_rate: float = 1e-4,
        weight_decay: float = 1e-5,
        lr_patience: int = 3,
        lr_factor: float = 0.5,
        minimum_lr: float = 1e-7,
        max_lr_reductions: int = 5,
        early_stop_patience: int = 10,
        gradient_clip: float = 1.0,
        checkpoint_interval: int = 10,
        epoch_interval: int = 10,
        input_dim: int = 400,
        d_model: int = 256,
        heads: int = 8,
        layers: int = 6,
        dropout: float = 0.10,
        seed: int = 42,
    ) -> TradingTransformer:

        print("\n" + "=" * 60)
        print(" INITIALIZING PRODUCTION TRAINING PIPELINE")
        print(f" Dataset Path: {path}")
        print("=" * 60 + "\n")

        # 1. Load chronological Train & Validation splits lazily
        train_dataset = FinalDataset(
            dataset_path=path,
            split="train",
            sequence_length=128,
            normalize=True,
        )

        validation_dataset = FinalDataset(
            dataset_path=path,
            split="validation",
            sequence_length=128,
            normalize=True,
        )

        if train_dataset.feature_dim != 400:
            raise ValueError(
                f"Expected 400 features, got {train_dataset.feature_dim}"
            )

        if train_dataset.sequence_length != 128:
            raise ValueError(
                f"Expected sequence length 128, got {train_dataset.sequence_length}"
            )

        feature_dim = 400
        sequence_length = 128

        print(f"\n[PRODUCTION] Feature dimension : {feature_dim}")
        print(f"[PRODUCTION] Sequence length   : {sequence_length}")
        print(f"[PRODUCTION] Train sequences   : {len(train_dataset):,}")
        print(f"[PRODUCTION] Val sequences     : {len(validation_dataset):,}")

        # 2. Instantiate TradingTransformer with configured architecture
        model = TradingTransformer(
            input_dim=feature_dim,
            d_model=d_model,
            heads=heads,
            layers=layers,
            dropout=dropout,
        )

        print(f"[PRODUCTION] Model parameters  : {model.num_parameters():,}")

        # 3. Create destination folders
        os.makedirs(drive_path, exist_ok=True)
        os.makedirs(os.path.dirname(save_path), exist_ok=True)

        production_dir = os.path.dirname(save_path)

        # 4. Initialize Trainer (with pre-split chronological datasets, NO random_split)
        trainer = Trainer(
            model=model,
            dataset=train_dataset,
            validation_dataset=validation_dataset,
            save_path=save_path,
            drive_path=drive_path,
            production_dir=production_dir,
            batch_size=batch_size,
            lr=learning_rate,
            weight_decay=weight_decay,
            max_epochs=max_epochs,
            min_epochs=min_epochs,
            lr_patience=lr_patience,
            lr_factor=lr_factor,
            minimum_lr=minimum_lr,
            maximum_lr_reduction=max_lr_reductions,
            early_stop_patience=early_stop_patience,
            gradient_clip=gradient_clip,
            checkpoint_interval=checkpoint_interval,
            epoch_interval=epoch_interval,
            resume=True,
            seed=seed,
        )

        # 5. Execute training loop
        trainer.train(max_epochs=max_epochs, min_epochs=min_epochs)

        # 6. Export production checkpoint
        ProductionCheckpoint().save(
            model,
            save_path,
        )

        print(f"\n[PRODUCTION] Final model successfully exported to: {save_path}")
        return model