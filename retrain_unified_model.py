from __future__ import annotations

import os
import torch
import torch.nn as nn
from torch.utils.data import TensorDataset, DataLoader

from app.settings import settings
from ai.model import TradingTransformer


def retrain():
    print("\n========================================================")
    print(" RETRAINING 48-FEATURE TRADING TRANSFORMER MODEL")
    print("========================================================\n")

    dataset_path = "dataset/unified_dataset.pt"

    if not os.path.exists(dataset_path):
        raise FileNotFoundError(f"Unified dataset file not found at {dataset_path}. Run generate_unified_dataset.py first.")

    data = torch.load(dataset_path)
    sequences = data["sequences"]
    labels = data["labels"]
    reversals = data["reversals"]
    volatilities = data["volatilities"]
    tps = data["take_profits"]
    sls = data["stop_losses"]
    feature_dim = data["feature_dim"]

    print(f"[RETRAIN] Loaded dataset: {tuple(sequences.shape)} features={feature_dim}")
    
    # Train / Validation Split (80% / 20%)
    split_idx = int(len(sequences) * 0.8)
    train_dataset = TensorDataset(
        sequences[:split_idx], labels[:split_idx], reversals[:split_idx], volatilities[:split_idx], tps[:split_idx], sls[:split_idx]
    )
    val_dataset = TensorDataset(
        sequences[split_idx:], labels[split_idx:], reversals[split_idx:], volatilities[split_idx:], tps[split_idx:], sls[split_idx:]
    )

    train_loader = DataLoader(train_dataset, batch_size=32, shuffle=True)
    val_loader = DataLoader(val_dataset, batch_size=32, shuffle=False)

    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    print(f"[RETRAIN] Using computation device: {device}")

    # Instantiate TradingTransformer with input_dim=48
    model = TradingTransformer(
        input_dim=feature_dim,
        d_model=256,
        heads=8,
        layers=6,
        dropout=0.10,
    ).to(device)

    # Class weights to prevent HOLD saturation (0: SELL, 1: HOLD, 2: BUY)
    class_weights = torch.tensor([2.5, 0.5, 2.5], dtype=torch.float32).to(device)
    criterion_signal = nn.CrossEntropyLoss(weight=class_weights)
    criterion_bce = nn.BCEWithLogitsLoss()
    criterion_mse = nn.MSELoss()

    optimizer = torch.optim.AdamW(model.parameters(), lr=1e-4, weight_decay=1e-4)

    epochs = 40
    best_val_loss = float("inf")
    save_path = settings.MODEL_PATH
    os.makedirs(os.path.dirname(save_path), exist_ok=True)

    print(f"\n[RETRAIN] Training for {epochs} epochs...")

    for epoch in range(1, epochs + 1):
        model.train()
        total_loss = 0.0
        correct_signal = 0
        total_samples = 0

        for batch_seq, batch_lbl, batch_rev, batch_vol, batch_tp, batch_sl in train_loader:
            batch_seq = batch_seq.to(device)
            batch_lbl = batch_lbl.to(device)
            batch_rev = batch_rev.to(device)
            batch_vol = batch_vol.to(device)
            batch_tp = batch_tp.to(device)
            batch_sl = batch_sl.to(device)

            optimizer.zero_grad()

            outputs = model(batch_seq)
            logits = outputs.get("signal_logits") if "signal_logits" in outputs else outputs.get("direction")

            loss_sig = criterion_signal(logits, batch_lbl)
            loss_vol = criterion_mse(outputs["volatility"].squeeze(), batch_vol)
            loss_tp = criterion_mse(outputs["take_profit"].squeeze(), batch_tp)
            loss_sl = criterion_mse(outputs["stop_loss"].squeeze(), batch_sl)

            loss = loss_sig + 0.2 * loss_vol + 0.3 * loss_tp + 0.3 * loss_sl

            loss.backward()
            torch.nn.utils.clip_grad_norm_(model.parameters(), max_norm=1.0)
            optimizer.step()

            total_loss += loss.item() * len(batch_lbl)
            preds = torch.argmax(logits, dim=-1)
            correct_signal += (preds == batch_lbl).sum().item()
            total_samples += len(batch_lbl)

        train_loss = total_loss / total_samples
        train_acc = correct_signal / total_samples

        # Validation
        model.eval()
        val_loss = 0.0
        val_correct = 0
        val_samples = 0

        with torch.no_grad():
            for batch_seq, batch_lbl, batch_rev, batch_vol, batch_tp, batch_sl in val_loader:
                batch_seq = batch_seq.to(device)
                batch_lbl = batch_lbl.to(device)
                batch_vol = batch_vol.to(device)
                batch_tp = batch_tp.to(device)
                batch_sl = batch_sl.to(device)

                outputs = model(batch_seq)
                logits = outputs.get("signal_logits") if "signal_logits" in outputs else outputs.get("direction")

                loss_sig = criterion_signal(logits, batch_lbl)
                loss_vol = criterion_mse(outputs["volatility"].squeeze(), batch_vol)
                loss_tp = criterion_mse(outputs["take_profit"].squeeze(), batch_tp)
                loss_sl = criterion_mse(outputs["stop_loss"].squeeze(), batch_sl)

                loss = loss_sig + 0.2 * loss_vol + 0.3 * loss_tp + 0.3 * loss_sl

                val_loss += loss.item() * len(batch_lbl)
                preds = torch.argmax(logits, dim=-1)
                val_correct += (preds == batch_lbl).sum().item()
                val_samples += len(batch_lbl)

        val_loss = val_loss / val_samples
        val_acc = val_correct / val_samples

        if epoch % 5 == 0 or epoch == 1:
            print(
                f"Epoch {epoch:2d}/{epochs:2d} | "
                f"Train Loss: {train_loss:.4f} Acc: {train_acc*100:.1f}% | "
                f"Val Loss: {val_loss:.4f} Acc: {val_acc*100:.1f}%"
            )

        if val_loss < best_val_loss:
            best_val_loss = val_loss
            torch.save(model.state_dict(), save_path)

    print(f"\n[RETRAIN SUCCESS] Best 48-feature model saved to: {save_path}")


if __name__ == "__main__":
    retrain()
