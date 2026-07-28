from training.production_train import ProductionTrain

#####################################################

# Dataset Location
DATASET_PATH = "data/processed/combined.npy"

# Final exported model
MODEL_PATH = "/content/drive/MyDrive/CryptoVisionAI/Production/production_v1.pt"

# Google Drive location
DRIVE_PATH = "/content/drive/MyDrive/CryptoVisionAI"

# Number of epochs
EPOCHS = 200

#####################################################


def main():

    print("\n")
    print("=" * 60)
    print("CRYPTO VISION AI")
    print("FINAL PRODUCTION TRAINING")
    print("=" * 60)

    trainer = ProductionTrain()

    trainer.train(

        path=DATASET_PATH,
        save_path=MODEL_PATH,
        drive_path=DRIVE_PATH,
        epochs=EPOCHS

    )

    print("\n")
    print("=" * 60)
    print("TRAINING COMPLETED")
    print("=" * 60)
    print(f"\nMODEL SAVED : {MODEL_PATH}")
    print("\n")


if __name__ == "__main__":
    main()