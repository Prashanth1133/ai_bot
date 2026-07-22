import torch
from torch.utils.data import Dataset


class TradingDataset(Dataset):

    """
    Sequence Dataset

    X:
        [samples, sequence, features]

    Labels:
        direction: 0 SELL
                   1 HOLD
                   2 BUY
    """

    def __init__(

        self,
        features,
        labels

    ):

        self.features = features
        self.labels = labels

    def __len__(self):

        return len(
            self.features
        )

    def __getitem__(
        self,
        idx
    ):

        x = torch.tensor(

            self.features[idx],

            dtype=torch.float32

        )

        y = {

            "direction":

                torch.tensor(

                    self.labels[idx]["direction"],

                    dtype=torch.long

                ),

            "confidence":

                torch.tensor(

                    self.labels[idx]["confidence"],

                    dtype=torch.float32

                ),

            "reversal":

                torch.tensor(

                    self.labels[idx]["reversal"],

                    dtype=torch.long

                ),

            "volatility":

                torch.tensor(

                    self.labels[idx]["volatility"],

                    dtype=torch.float32

                ),

            "take_profit":

                torch.tensor(

                    self.labels[idx]["take_profit"],

                    dtype=torch.float32

                ),

            "stop_loss":

                torch.tensor(

                    self.labels[idx]["stop_loss"],

                    dtype=torch.float32

                ),

            "market_regime":

                torch.tensor(

                    self.labels[idx]["market_regime"],

                    dtype=torch.long

                )

        }

        return x, y