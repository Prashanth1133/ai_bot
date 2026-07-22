import torch
from torch.utils.data import Dataset


class TradingDataset(Dataset):

    def __init__(self, dataframe):

        self.df = dataframe

    def __len__(self):

        return len(self.df)

    def __getitem__(self, index):

        row = self.df.iloc[index]

        return {

            "sequence":

                torch.tensor(

                    row.sequence,

                    dtype=torch.float32

                ),

            "direction":

                torch.tensor(

                    row.direction

                ),

            "confidence":

                torch.tensor(

                    row.confidence,

                    dtype=torch.float32

                ),

            "tp":

                torch.tensor(

                    row.tp,

                    dtype=torch.float32

                ),

            "sl":

                torch.tensor(

                    row.sl,

                    dtype=torch.float32

                ),

            "regime":

                torch.tensor(

                    row.regime

                )
        }