import os
import joblib
import numpy as np

from sklearn.preprocessing import StandardScaler


def main():

    # ----------------------------------------------------
    # IMPORTANT:
    # Update this later after counting all AI features.
    # For now, we use 64 features for V1.
    # ----------------------------------------------------

    NUM_FEATURES = 64

    # Create dummy training data
    X = np.random.rand(
        10000,
        NUM_FEATURES,
    )

    # Train scaler
    scaler = StandardScaler()

    scaler.fit(
        X
    )

    # Create models directory
    os.makedirs(
        "models",
        exist_ok=True,
    )

    # Save scaler
    joblib.dump(
        scaler,
        "models/scaler.pkl",
    )

    print(
        "\nScaler trained successfully!"
    )

    print(
        f"Features : {NUM_FEATURES}"
    )

    print(
        "Saved    : models/scaler.pkl"
    )


if __name__ == "__main__":
    main()