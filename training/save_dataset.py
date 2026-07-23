import os
import numpy as np


def save_dataset(

    path,
    data

):

    directory = os.path.dirname(path)

    os.makedirs(

        directory,

        exist_ok=True

    )

    np.save(

        path,
        data,
        allow_pickle=True

    )

    print(

        f"Saved -> {path}"

    )