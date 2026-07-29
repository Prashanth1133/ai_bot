from ai.model import TradingTransformer
from ai.dataset import TradingDataset
from ai.trainer import Trainer


def train(

    features,
    labels

):

    input_dim = len(

        features[0][0]

    )

    model = TradingTransformer(

        input_dim=input_dim

    )

    dataset = TradingDataset(

        features,

        labels

    )

    trainer = Trainer(

        model,

        dataset

    )

    trainer.train(

        epochs=200

    )

    return model