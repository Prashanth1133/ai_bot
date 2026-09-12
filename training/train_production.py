from __future__ import annotations

import os
from training.production_train import ProductionTrain

# ============================================================
# FINAL PRODUCTION TRAINING CONFIGURATION
# ============================================================

# Dataset Location (128 sequence length, 400 point-in-time features)
DATASET_PATH = "dataset/final_unified_dataset.pt"

# Google Drive storage root
DRIVE_PATH = "/content/drive/MyDrive/CryptoVisionAI"

# Final exported model location (versioned)
MODEL_PATH = (
    "/content/drive/MyDrive/"
    "CryptoVisionAI/"
    "Production/"
    "BTCUSDT/"
    "final_v1/"
    "final_model.pt"
)

# ============================================================
# TRAINING BUDGET & CONVERGENCE CONTROL
# ============================================================

MAX_EPOCHS = 100
MIN_EPOCHS = 10

BATCH_SIZE = 256
LEARNING_RATE = 1e-4
WEIGHT_DECAY = 1e-5

LR_PATIENCE = 3
LR_FACTOR = 0.5
MINIMUM_LR = 1e-7
MAX_LR_REDUCTIONS = 5

EARLY_STOP_PATIENCE = 10
GRADIENT_CLIP = 1.0

CHECKPOINT_INTERVAL = 10
EPOCH_INTERVAL = 10

SEQUENCE_LENGTH = 128
INPUT_DIM = 400
D_MODEL = 256
HEADS = 8
LAYERS = 6
DROPOUT = 0.10

SEED = 42

# ============================================================


def main():
    print("\n" + "=" * 60)
    print(" CRYPTO VISION AI - PRODUCTION TRAINING")
    print(" 400-FEATURE MULTI-TASK TRANSFORMER PIPELINE")
    print("=" * 60)

    dataset_file = DATASET_PATH
    if not os.path.exists(dataset_file) and os.path.exists("data/processed/final_unified_dataset.pt"):
        dataset_file = "data/processed/final_unified_dataset.pt"

    drive_location = DRIVE_PATH
    model_save_path = MODEL_PATH

    # If running locally outside Colab without /content/drive mounted:
    if not os.path.exists("/content/drive"):
        drive_location = os.path.abspath("models")
        model_save_path = os.path.abspath("models/Production/BTCUSDT/final_v1/final_model.pt")

    trainer = ProductionTrain()

    trainer.train(
        path=dataset_file,
        save_path=model_save_path,
        drive_path=drive_location,
        max_epochs=MAX_EPOCHS,
        min_epochs=MIN_EPOCHS,
        batch_size=BATCH_SIZE,
        learning_rate=LEARNING_RATE,
        weight_decay=WEIGHT_DECAY,
        lr_patience=LR_PATIENCE,
        lr_factor=LR_FACTOR,
        minimum_lr=MINIMUM_LR,
        max_lr_reductions=MAX_LR_REDUCTIONS,
        early_stop_patience=EARLY_STOP_PATIENCE,
        gradient_clip=GRADIENT_CLIP,
        checkpoint_interval=CHECKPOINT_INTERVAL,
        epoch_interval=EPOCH_INTERVAL,
        input_dim=INPUT_DIM,
        d_model=D_MODEL,
        heads=HEADS,
        layers=LAYERS,
        dropout=DROPOUT,
        seed=SEED,
    )

    print("\n" + "=" * 60)
    print(" TRAINING COMPLETED")
    print("=" * 60)
    print(f"\nMODEL SAVED : {model_save_path}\n")


if __name__ == "__main__":
    main()