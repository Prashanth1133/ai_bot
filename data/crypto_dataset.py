import torch
from torch.utils.data import Dataset


class CryptoDataset(Dataset):

    def __init__(
        self,
        X,
        y
    ):

        self.X = torch.tensor(
            X,
            dtype=torch.float32
        )

        self.y = y

    def __len__(self):

        return len(self.X)

    def __getitem__(
        self,
        idx
    ):

        sample = {}

        for key, value in self.y.items():

            if key in [

                "direction",
                "reversal",
                "market_regime"

            ]:

                sample[key] = torch.tensor(

                    value[idx],

                    dtype=torch.long

                )

            else:

                sample[key] = torch.tensor(

                    value[idx],

                    dtype=torch.float32

                )

        return (

            self.X[idx],

            sample

        )