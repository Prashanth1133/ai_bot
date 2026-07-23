from torch.utils.data import (
    DataLoader
)


class ProductionLoader:


    def build(

        self,
        dataset,
        batch_size=64

    ):


        return DataLoader(

            dataset,

            batch_size=batch_size,

            shuffle=True,

            drop_last=False

        )