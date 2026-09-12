from __future__ import annotations

import argparse
import os
import sys
from pathlib import Path

import torch
from torch.utils.data import DataLoader

from ai.dataset import load_chronological_datasets
from ai.model import TradingTransformer
from ai.trainer import Trainer
from evaluation.metrics import Metrics


def run_smoke_test(
    dataset_path: str = "dataset/final_unified_dataset_v7.pt",
    production_dir: str = "models/Production/BTCUSDT/smoke_test",
) -> None:
    print("\n" + "=" * 70)
    print(" STEP 4: RUNNING 2-EPOCH TRAINING SMOKE TEST")
    print("=" * 70)

    train_ds, val_ds, _ = load_chronological_datasets(dataset_path)

    model = TradingTransformer(
        input_dim=48,
        d_model=256,
        heads=8,
        layers=6,
        dropout=0.10,
    )

    trainer = Trainer(
        model=model,
        dataset=train_ds,
        validation_dataset=val_ds,
        production_dir=production_dir,
        batch_size=32,
        lr=1e-4,
        max_epochs=2,
        min_epochs=1,
        early_stop_patience=5,
        checkpoint_interval=1,
        epoch_interval=1,
        resume=False,
    )

    trainer.train(max_epochs=2)
    print("\n[SMOKE TEST COMPLETE] Verifying checkpoint creation in:", production_dir)


def run_production_training(
    dataset_path: str = "dataset/final_unified_dataset_v7.pt",
    production_dir: str = "models/Production/BTCUSDT/final_v1",
    max_epochs: int = 100,
    min_epochs: int = 10,
    batch_size: int = 64,
    lr: float = 1e-4,
    early_stop_patience: int = 10,
    resume: bool = False,
) -> None:
    print("\n" + "=" * 70)
    print(" STEP 6: STARTING PRODUCTION 15-DAY TRANSFORMER TRAINING")
    print("=" * 70)

    train_ds, val_ds, _ = load_chronological_datasets(dataset_path)

    model = TradingTransformer(
        input_dim=48,
        d_model=256,
        heads=8,
        layers=6,
        dropout=0.10,
    )

    trainer = Trainer(
        model=model,
        dataset=train_ds,
        validation_dataset=val_ds,
        production_dir=production_dir,
        batch_size=batch_size,
        lr=lr,
        max_epochs=max_epochs,
        min_epochs=min_epochs,
        early_stop_patience=early_stop_patience,
        checkpoint_interval=10,
        epoch_interval=10,
        resume=resume,
    )

    trainer.train(max_epochs=max_epochs)
    print("\n[PRODUCTION TRAINING COMPLETE] Best model saved to:", trainer.best_save_path)


def evaluate_test_set(
    dataset_path: str = "dataset/final_unified_dataset_v7.pt",
    model_path: str = "models/Production/BTCUSDT/final_v1/best_model.pt",
    batch_size: int = 64,
) -> None:
    print("\n" + "=" * 70)
    print(" STEP 8 & 9: BENCHMARKING UNTOUCHED TEST SET (2,505 SAMPLES)")
    print("=" * 70)

    _, _, test_ds = load_chronological_datasets(dataset_path)
    test_loader = DataLoader(test_ds, batch_size=batch_size, shuffle=False)

    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    model = TradingTransformer(input_dim=48, d_model=256, heads=8, layers=6, dropout=0.10)

    if not os.path.exists(model_path):
        raise FileNotFoundError(f"Model weights not found at: {model_path}")

    state_dict = torch.load(model_path, map_location=device)
    model.load_state_dict(state_dict)
    model.to(device)
    model.eval()

    all_dir_preds, all_dir_targets, all_dir_probs = [], [], []
    all_rev_preds, all_rev_targets = [], []
    all_ret15_preds, all_ret15_targets = [], []
    all_ret1h_preds, all_ret1h_targets = [], []
    all_ret4h_preds, all_ret4h_targets = [], []
    all_tp_preds, all_tp_targets = [], []
    all_sl_preds, all_sl_targets = [], []

    with torch.no_grad():
        for x, y in test_loader:
            x = x.to(device)
            outputs = model(x)

            # Direction
            probs = torch.softmax(outputs["direction"], dim=-1).cpu().numpy()
            preds = torch.argmax(outputs["direction"], dim=-1).cpu().numpy()
            all_dir_probs.extend(probs)
            all_dir_preds.extend(preds)
            all_dir_targets.extend(y["direction"].numpy())

            # Reversal
            all_rev_preds.extend(torch.sigmoid(outputs["reversal"]).squeeze(-1).cpu().numpy())
            all_rev_targets.extend(y["reversal"].numpy())

            # Returns
            all_ret15_preds.extend(outputs["return_15m"].squeeze(-1).cpu().numpy())
            all_ret15_targets.extend(y["return_15m"].numpy())

            all_ret1h_preds.extend(outputs["return_1h"].squeeze(-1).cpu().numpy())
            all_ret1h_targets.extend(y["return_1h"].numpy())

            all_ret4h_preds.extend(outputs["return_4h"].squeeze(-1).cpu().numpy())
            all_ret4h_targets.extend(y["return_4h"].numpy())

            # Risk
            all_tp_preds.extend(outputs["take_profit"].squeeze(-1).cpu().numpy())
            all_tp_targets.extend(y["take_profit"].numpy())

            all_sl_preds.extend(outputs["stop_loss"].squeeze(-1).cpu().numpy())
            all_sl_targets.extend(y["stop_loss"].numpy())

    import numpy as np

    dir_metrics = Metrics.classification_metrics(all_dir_targets, all_dir_preds, num_classes=3, class_names=["SELL", "HOLD", "BUY"])
    rev_metrics = Metrics.reversal_metrics(all_rev_targets, all_rev_preds)

    print("\n" + "=" * 70)
    print(" TEST SET BENCHMARK RESULTS")
    print("=" * 70)
    print(f" Total Test Samples : {len(all_dir_targets):,}")
    print(f" Overall Accuracy   : {dir_metrics['accuracy'] * 100:.2f}%")
    print(f" Macro F1 Score     : {dir_metrics['macro_f1']:.4f}")
    print("\n Direction Classification Breakdown:")
    for cls_name, p in dir_metrics["per_class"].items():
        print(f"   {cls_name:<4} -> Precision: {p['precision']*100:5.2f}% | Recall: {p['recall']*100:5.2f}% | F1: {p['f1']:.4f} | Support: {p['support']:,}")

    print("\n Reversal Detection Breakdown:")
    print(f"   Accuracy : {rev_metrics['accuracy']*100:5.2f}% | Precision: {rev_metrics['precision']*100:5.2f}% | Recall: {rev_metrics['recall']*100:5.2f}% | F1: {rev_metrics['f1']:.4f}")

    ret15_mae = float(np.mean(np.abs(np.array(all_ret15_preds) - np.array(all_ret15_targets))))
    ret1h_mae = float(np.mean(np.abs(np.array(all_ret1h_preds) - np.array(all_ret1h_targets))))
    ret4h_mae = float(np.mean(np.abs(np.array(all_ret4h_preds) - np.array(all_ret4h_targets))))
    tp_mae = float(np.mean(np.abs(np.array(all_tp_preds) - np.array(all_tp_targets))))
    sl_mae = float(np.mean(np.abs(np.array(all_sl_preds) - np.array(all_sl_targets))))

    print("\n Regression MAE Errors:")
    print(f"   Return 15m MAE : {ret15_mae:.5f}")
    print(f"   Return 1h  MAE : {ret1h_mae:.5f}")
    print(f"   Return 4h  MAE : {ret4h_mae:.5f}")
    print(f"   Take Profit MAE: {tp_mae:.5f}")
    print(f"   Stop Loss   MAE: {sl_mae:.5f}")

    # Trading-oriented metrics simulation
    targets_np = np.array(all_dir_targets)
    preds_np = np.array(all_dir_preds)
    returns_1h_np = np.array(all_ret1h_targets)

    buy_signals = int(np.sum(preds_np == 2))
    sell_signals = int(np.sum(preds_np == 0))
    hold_signals = int(np.sum(preds_np == 1))

    # PnL simulation: Long when BUY (return = ret_1h), Short when SELL (return = -ret_1h)
    trade_returns = []
    win_trades = 0
    total_trades = 0

    for i in range(len(preds_np)):
        if preds_np[i] == 2:  # BUY
            ret = returns_1h_np[i]
            trade_returns.append(ret)
            total_trades += 1
            if ret > 0:
                win_trades += 1
        elif preds_np[i] == 0:  # SELL
            ret = -returns_1h_np[i]
            trade_returns.append(ret)
            total_trades += 1
            if ret > 0:
                win_trades += 1

    win_rate = (win_trades / total_trades * 100) if total_trades > 0 else 0.0
    gains = [r for r in trade_returns if r > 0]
    losses = [abs(r) for r in trade_returns if r < 0]
    profit_factor = (sum(gains) / sum(losses)) if sum(losses) > 0 else (float("inf") if sum(gains) > 0 else 0.0)
    avg_return_per_trade = float(np.mean(trade_returns)) * 100 if trade_returns else 0.0

    print("\n" + "=" * 70)
    print(" TRADING-ORIENTED SIMULATION BENCHMARK (1h Execution)")
    print("=" * 70)
    print(f" Total Signals Generated: {len(preds_np):,}")
    print(f"   BUY  Signals         : {buy_signals:,} ({buy_signals/len(preds_np)*100:.1f}%)")
    print(f"   SELL Signals         : {sell_signals:,} ({sell_signals/len(preds_np)*100:.1f}%)")
    print(f"   HOLD Signals         : {hold_signals:,} ({hold_signals/len(preds_np)*100:.1f}%)")
    print(f" Total Executed Trades  : {total_trades:,}")
    print(f" Win Rate               : {win_rate:.2f}%")
    print(f" Profit Factor          : {profit_factor:.3f}")
    print(f" Avg Return per Trade   : {avg_return_per_trade:+.3f}%")
    print("=" * 70 + "\n")


def main():
    parser = argparse.ArgumentParser(description="CryptoVisionAI Transformer Training Pipeline")
    parser.add_argument("--smoke-test", action="store_true", help="Run 2-epoch smoke test to verify training path")
    parser.add_argument("--full", action="store_true", help="Run full production transformer training")
    parser.add_argument("--eval-test", action="store_true", help="Run benchmark on untouched test partition")
    parser.add_argument("--dataset", type=str, default="dataset/final_unified_dataset_v7.pt", help="Path to dataset bundle")
    parser.add_argument("--epochs", type=int, default=100, help="Maximum epochs for production training")
    parser.add_argument("--min-epochs", type=int, default=10, help="Minimum epochs for production training")
    parser.add_argument("--batch-size", type=int, default=64, help="Batch size")
    parser.add_argument("--lr", type=float, default=1e-4, help="Learning rate")
    parser.add_argument("--early-stop", type=int, default=10, help="Early stopping patience")
    parser.add_argument("--resume", action="store_true", help="Resume from existing checkpoint")

    args = parser.parse_args()

    if args.smoke_test:
        run_smoke_test(dataset_path=args.dataset)
    elif args.eval_test:
        evaluate_test_set(dataset_path=args.dataset)
    elif args.full:
        run_production_training(
            dataset_path=args.dataset,
            max_epochs=args.epochs,
            min_epochs=args.min_epochs,
            batch_size=args.batch_size,
            lr=args.lr,
            early_stop_patience=args.early_stop,
            resume=args.resume,
        )
    else:
        # Default behavior: run smoke test first for safety
        run_smoke_test(dataset_path=args.dataset)


if __name__ == "__main__":
    main()

