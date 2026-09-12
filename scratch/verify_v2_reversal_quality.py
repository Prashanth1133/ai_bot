import torch
import numpy as np

PATH = "dataset/final_unified_dataset_structural_reversal.pt"

print("=" * 80)
print("V2 STRUCTURAL REVERSAL QUALITY AUDIT")
print("=" * 80)

bundle = torch.load(
    PATH,
    map_location="cpu",
    weights_only=False
)

for split in ["train", "validation", "test"]:
    data = bundle[split]
    reversal = None

    if isinstance(data, dict):
        if "reversal" in data:
            reversal = data["reversal"]
        elif "labels" in data and isinstance(data["labels"], dict):
            reversal = data["labels"]["reversal"]
        elif "targets" in data and isinstance(data["targets"], dict):
            reversal = data["targets"]["reversal"]

    if reversal is None:
        print(f"\n{split.upper()}: reversal target not directly accessible")
        continue

    reversal = np.asarray(reversal)
    zeros = int(np.sum(reversal == 0))
    ones = int(np.sum(reversal == 1))
    total = len(reversal)

    print(f"\n[{split.upper()}]")
    print(f"Total          : {total:,}")
    print(f"NON-REVERSAL(0): {zeros:,} ({100 * zeros / total:.3f}%)")
    print(f"REVERSAL(1)    : {ones:,} ({100 * ones / total:.3f}%)")
    print(f"Majority Base  : {max(zeros, ones) / total * 100:.3f}%")

    if split == "train" and ones > 0:
        pos_weight = zeros / ones
        print(f"Calculated BCE pos_weight: {pos_weight:.4f}")

    if ones == 0 or zeros == 0:
        print("RESULT: FAIL (SINGLE-CLASS REVERSAL LABEL)")
    elif ones / total > 0.80:
        print("RESULT: FAIL (REVERSAL STILL TOO DOMINANT > 80%)")
    elif ones / total < 0.02:
        print("RESULT: WARNING (REVERSAL VERY RARE < 2%)")
    else:
        print("RESULT: PASS (REVERSAL DISTRIBUTION IS BALANCED & TRAINABLE)")

print("\n" + "=" * 80)
