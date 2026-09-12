import torch
from collections import Counter

DATASET = "dataset/final_unified_dataset_structural_reversal.pt"

print("=" * 80)
print("STRUCTURAL REVERSAL DATASET AUDIT")
print("=" * 80)

data = torch.load(DATASET, map_location="cpu", weights_only=False)

print("\nTop-level keys:")
for k in data.keys():
    print(" ", k)

if "metadata" in data and "label_configuration" in data["metadata"]:
    print("\nLabel Configuration in Metadata:")
    import json
    print(json.dumps(data["metadata"]["label_configuration"], indent=2))
elif "label_configuration" in data:
    import json
    print("\nLabel Configuration:")
    print(json.dumps(data["label_configuration"], indent=2))

names = {0: "SELL", 1: "HOLD", 2: "BUY"}

for split_name in ["train", "validation", "test"]:
    if split_name not in data:
        continue

    split = data[split_name]
    print("\n" + "=" * 80)
    print(split_name.upper())
    print("=" * 80)

    direction = split["direction"]
    if torch.is_tensor(direction):
        direction = direction.cpu().numpy()

    direction_counts = Counter(direction.tolist())
    total = len(direction)

    print("\nDIRECTION")
    print("-" * 50)
    for cls in [0, 1, 2]:
        count = direction_counts.get(cls, 0)
        pct = count / total * 100
        print(f"{cls} {names[cls]:5s}: {count:10,d} {pct:8.3f}%")

    reversal = split["reversal"]
    if torch.is_tensor(reversal):
        reversal = reversal.cpu()
    reversal = reversal.reshape(-1)

    zeros = int((reversal == 0).sum())
    ones = int((reversal == 1).sum())
    total_r = zeros + ones

    print("\nSTRUCTURAL REVERSAL")
    print("-" * 50)
    print(f"0 = NON-REVERSAL : {zeros:10,d} {zeros / total_r * 100:8.3f}%")
    print(f"1 = REVERSAL     : {ones:10,d} {ones / total_r * 100:8.3f}%")
    print(f"Majority baseline: {max(zeros, ones) / total_r * 100:.3f}%")

    # Pos weight for BCE loss on train split
    if split_name == "train" and ones > 0:
        pos_weight = zeros / ones
        print(f"Computed pos_weight for BCEWithLogitsLoss: {pos_weight:.4f}")

    print("\nREVERSAL BY DIRECTION")
    print("-" * 50)
    for d in [0, 1, 2]:
        mask = (torch.tensor(direction) == d)
        r = reversal[mask]
        if len(r) == 0:
            continue
        r0 = int((r == 0).sum())
        r1 = int((r == 1).sum())
        print(f"{names[d]:5s}: non-reversal={r0:,} ({r0/len(r)*100:.2f}%) reversal={r1:,} ({r1/len(r)*100:.2f}%)")

    print("\nREGRESSION TARGET SUMMARY")
    print("-" * 50)
    for name in ["return_15m", "return_1h", "return_4h", "max_return_1h", "min_return_1h", "take_profits", "stop_losses"]:
        if name in split:
            x = split[name].float().reshape(-1)
            print(f"{name:18s} min={x.min().item(): .6f} max={x.max().item(): .6f} mean={x.mean().item(): .6f} std={x.std().item(): .6f}")

print("\n" + "=" * 80)
print("AUDIT COMPLETE")
print("=" * 80)
