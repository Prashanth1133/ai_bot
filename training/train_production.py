from training.production_train import (
    ProductionTrain
)


DATASET_PATH = (

    "data/processed/combined.npy"

)


MODEL_PATH = (

    "models/production_v1.pt"

)


EPOCHS = 200

def main():

    print("\n")

    print("="*60)
    print("CRYPTO VISION AI")
    print("PRODUCTION V1 TRAINING")
    print("="*60)


    trainer = (

        ProductionTrain()

    )


    trainer.train(

        path=DATASET_PATH,

        save_path=MODEL_PATH,

        epochs=EPOCHS

    )


    print("\n")

    print("="*60)
    print("TRAINING COMPLETED")
    print("="*60)

    print(

        f"\nMODEL SAVED : {MODEL_PATH}"

    )

    print("\n")


if __name__ == "__main__":

    main()