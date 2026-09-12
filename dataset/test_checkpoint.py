from pathlib import Path
import numpy as np


CHECKPOINT_DIR = Path("dataset/checkpoints")
CHECKPOINT_DIR.mkdir(parents=True, exist_ok=True)

TEST_FILE = CHECKPOINT_DIR / "BTCUSDT_checkpoint_test.npz"


# Create a small test matrix
original = np.random.rand(100, 48).astype(np.float32)

print("=" * 60)
print("CHECKPOINT TEST")
print("=" * 60)

print(f"Original shape : {original.shape}")
print(f"Test file      : {TEST_FILE}")

# ------------------------------------------------------------
# SAVE
# ------------------------------------------------------------

np.savez_compressed(
    TEST_FILE,
    feature_matrix=original,
)

print()
print("[1/3] SAVE")
print(f"Exists         : {TEST_FILE.exists()}")

if TEST_FILE.exists():
    print(
        f"File size      : "
        f"{TEST_FILE.stat().st_size:,} bytes"
    )
else:
    raise RuntimeError("Checkpoint was NOT created!")

# ------------------------------------------------------------
# LOAD
# ------------------------------------------------------------

print()
print("[2/3] LOAD")

with np.load(
    TEST_FILE,
    allow_pickle=False,
) as data:

    restored = data["feature_matrix"]

print(f"Restored shape : {restored.shape}")
print(f"Restored dtype : {restored.dtype}")

# ------------------------------------------------------------
# VERIFY
# ------------------------------------------------------------

print()
print("[3/3] VERIFY")

if np.array_equal(original, restored):
    print("SUCCESS: Checkpoint save/load works.")
else:
    raise RuntimeError(
        "FAILURE: Restored data differs from original."
    )

print("=" * 60)