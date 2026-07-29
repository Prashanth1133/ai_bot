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
        checkpoint_interval=50,
        early_stop_patience=12,
    )

    trainer.train(
        epochs=200
    )


if __name__ == "__main__":
    main()
