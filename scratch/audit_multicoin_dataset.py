import torch
import numpy as np
from collections import Counter

PATH = "dataset/final_unified_dataset_v2.pt"

print("=" * 80)
print("MULTI-COIN V2 DATASET FORENSIC AUDIT (BTC + ETH + DOGE)")
print("=" * 80)

bundle = torch.load(PATH, map_location="cpu", weights_only=False)

symbols = bundle.get("symbols", ["BTCUSDT", "ETHUSDT", "DOGEUSDT"])
print(f"\nSymbols in dataset: {symbols}")
print(f"Dataset version   : {bundle.get('dataset_version')}")
print(f"Label version     : {bundle.get('label_version')}")
print(f"Feature dimension : {bundle.get('feature_dim')}")
print(f"Sequence length   : {bundle.get('sequence_length')}")

direction_names = {0: "SELL", 1: "HOLD", 2: "BUY"}

# Overall combined stats
combined_counts = {
    "train": {"dir": Counter(), "rev": Counter(), "total": 0},
    "validation": {"dir": Counter(), "rev": Counter(), "total": 0},
    "test": {"dir": Counter(), "rev": Counter(), "total": 0},
}

for sym in symbols:
    print("\n" + "#" * 80)
    print(f" COIN AUDIT: {sym}")
    print("#" * 80)

    coin_data = bundle.get(sym, {})
    for split in ["train", "validation", "test"]:
        if split not in coin_data:
            continue
        data = coin_data[split]
        print(f"\n--- {sym} [{split.upper()}] ---")

        features = data["features"]
        direction = np.asarray(data["direction"])
        reversal = np.asarray(data["reversal"])

        total = len(direction)
        print(f"Samples: {total:,} | Feature shape: {tuple(features.shape)}")

        # Check NaNs / Infs
        nan_feat = torch.isnan(features).sum().item()
        inf_feat = torch.isinf(features).sum().item()
        print(f"Feature NaN/Inf: NaNs={nan_feat}, Infs={inf_feat}")

        # Direction distribution
        d_counts = Counter(direction.tolist())
        print("\n  DIRECTION:")
        for k in [0, 1, 2]:
            c = d_counts.get(k, 0)
            print(f"    {k} {direction_names[k]:5s}: {c:10,d} ({100.0 * c / total:6.2f}%)")
            combined_counts[split]["dir"][k] += c

        # Reversal distribution
        r_zeros = int(np.sum(reversal == 0))
        r_ones = int(np.sum(reversal == 1))
        print("\n  STRUCTURAL REVERSAL:")
        print(f"    0 (Non-Rev): {r_zeros:10,d} ({100.0 * r_zeros / total:6.2f}%)")
        print(f"    1 (Reversal): {r_ones:10,d} ({100.0 * r_ones / total:6.2f}%)")
        combined_counts[split]["rev"][0] += r_zeros
        combined_counts[split]["rev"][1] += r_ones
        combined_counts[split]["total"] += total

        if split == "train" and r_ones > 0:
            pw = r_zeros / r_ones
            print(f"    pos_weight (BCE) = {pw:.4f}")

        # Reversal by direction cross-tab
        print("\n  REVERSAL BY DIRECTION:")
        for d in [0, 1, 2]:
            mask = (direction == d)
            r_sub = reversal[mask]
            if len(r_sub) > 0:
                s_rev = int(np.sum(r_sub == 1))
                print(f"    {direction_names[d]:5s}: reversal={s_rev:,}/{len(r_sub):,} ({100.0 * s_rev / len(r_sub):.2f}%)")

        # Regression stats
        print("\n  REGRESSION SUMMARY:")
        for t_name in ["return_15m", "return_1h", "return_4h", "max_return_1h", "min_return_1h", "take_profits", "stop_losses"]:
            if t_name in data:
                arr = np.asarray(data[t_name])
                print(f"    {t_name:16s} min={arr.min(): .5f} max={arr.max(): .5f} mean={arr.mean(): .5f} std={arr.std(): .5f}")

print("\n" + "=" * 80)
print(" COMBINED (BTC + ETH + DOGE) SUMMARY")
print("=" * 80)
for split in ["train", "validation", "test"]:
    st = combined_counts[split]
    tot = st["total"]
    print(f"\n[{split.upper()}] (Total Sequences = {tot:,})")
    print("  Direction:")
    for k in [0, 1, 2]:
        c = st["dir"][k]
        print(f"    {direction_names[k]:5s}: {c:10,d} ({100.0 * c / tot:6.2f}%)")
    r0 = st["rev"][0]
    r1 = st["rev"][1]
    print(f"  Structural Reversal: 0={r0:,} ({100.0*r0/tot:.2f}%), 1={r1:,} ({100.0*r1/tot:.2f}%)")
    if split == "train" and r1 > 0:
        print(f"  Combined Train BCE pos_weight: {r0/r1:.4f}")

print("\n" + "=" * 80)
print("AUDIT COMPLETE")
print("=" * 80)
