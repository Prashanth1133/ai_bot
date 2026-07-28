from ai.model import Model
from ai.dataset import Dataset
from ai.trainer import Trainer


def main():
    model = Model()

    dataset = Dataset()

    trainer = Trainer(
        model=model,
        dataset=dataset,
        resume=True,
        checkpoint_interval=20,
        early_stop_patience=25,
    )

    trainer.train(
        epochs=500
    )


if __name__ == "__main__":
    main()
