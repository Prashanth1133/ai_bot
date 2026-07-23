import os
import numpy as np


def load_dataset(

    path

):

    if not os.path.exists(path):

        raise FileNotFoundError(

            f"\nDataset Not Found : {path}"

        )

    data = np.load(

        path,

        allow_pickle=True

    )

    return data