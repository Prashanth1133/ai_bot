import torch
import numpy as np

V1 = "dataset/final_unified_dataset.pt"
V2 = "dataset/final_unified_dataset_structural_reversal.pt"


def load(path):
    print(f"\nLoading: {path}")
    return torch.load(path, map_location="cpu", weights_only=False)


def inspect(bundle, name):
    print("\n" + "=" * 80)
    print(name)
    print("=" * 80)
    print("Keys:", list(bundle.keys()))

    for split in ["train", "validation", "test"]:
        if split not in bundle:
            continue
        data = bundle[split]
        print(f"\n[{split.upper()}]")
        if isinstance(data, dict):
            for key in data:
                value = data[key]
                if torch.is_tensor(value):
                    print(f"  {key:20s} {tuple(value.shape)} {value.dtype}")


def main():
    v1 = load(V1)
    v2 = load(V2)

    inspect(v1, "V1 (BASELINE)")
    inspect(v2, "V2 (STRUCTURAL REVERSAL)")

    print("\n" + "=" * 80)
    print("V1 vs V2 FROZEN LABEL COMPARISON AUDIT")
    print("=" * 80)

    for split in ["train", "validation", "test"]:
        print(f"\n===== {split.upper()} =====")
        a = v1[split]
        b = v2[split]

        if isinstance(a, dict) and isinstance(b, dict):
            keys = set(a.keys()) & set(b.keys())
            for key in sorted(keys):
                if key in ["reversal"]:
                    continue
                try:
                    x = np.asarray(a[key])
                    y = np.asarray(b[key])

                    same = np.array_equal(x, y)
                    print(f"  {key:20s}: {'UNCHANGED (IDENTICAL)' if same else 'CHANGED'}")
                    if not same:
                        diff = np.sum(x != y)
                        print(f"    WARNING: differing elements: {diff}")
                except Exception as e:
                    print(f"  {key:20s}: comparison failed: {e}")

        # Show reversal change
        r1 = np.asarray(a["reversal"])
        r2 = np.asarray(b["reversal"])
        r1_ones = np.sum(r1 == 1)
        r2_ones = np.sum(r2 == 1)
        print(f"\n  REVERSAL COMPARISON:")
        print(f"    V1 Reversal % : {r1_ones / len(r1) * 100:.3f}% ({r1_ones:,}/{len(r1):,})")
        print(f"    V2 Reversal % : {r2_ones / len(r2) * 100:.3f}% ({r2_ones:,}/{len(r2):,})")


if __name__ == "__main__":
    main()
