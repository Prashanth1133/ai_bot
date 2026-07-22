import os
import torch


class ModelManager:

    """
    Handles:

    - Saving models
    - Loading models
    - Registering multiple models
    - Performing inference
    """

    def __init__(self):

        self.models = {}

    def register(

        self,
        name,
        model

    ):

        self.models[name] = model

    def save(

        self,
        name,
        path=None

    ):

        if name not in self.models:

            raise ValueError(

                f"Model '{name}' not registered."

            )

        if path is None:

            path = f"models/{name}.pt"

        os.makedirs(

            os.path.dirname(path),

            exist_ok=True

        )

        torch.save(

            self.models[name].state_dict(),

            path

        )

        print(

            f"Saved {name} -> {path}"

        )

    def load(

        self,
        name,
        path

    ):

        if name not in self.models:

            raise ValueError(

                f"Model '{name}' not registered."

            )

        if not os.path.exists(path):

            print(

                f"Model not found: {path}"

            )

            return False

        self.models[name].load_state_dict(

            torch.load(

                path,

                map_location="cpu"

            )

        )

        self.models[name].eval()

        print(

            f"Loaded {name} <- {path}"

        )

        return True

    def get(

        self,
        name

    ):

        if name not in self.models:

            raise KeyError(

                f"{name} not registered."

            )

        return self.models[name]

    def predict(

        self,
        name,
        features

    ):

        if name not in self.models:

            raise KeyError(

                f"{name} not registered."

            )

        model = self.models[name]

        model.eval()

        with torch.no_grad():

            if not isinstance(

                features,

                torch.Tensor

            ):

                features = torch.tensor(

                    features,

                    dtype=torch.float32

                )

            if len(

                features.shape

            ) == 2:

                features = (

                    features.unsqueeze(0)

                )

            outputs = model(

                features

            )

            direction = torch.softmax(

                outputs["direction"],

                dim=-1

            )

            confidence = float(

                direction.max()

            )

            signal = int(

                direction.argmax()

            )

            mapping = {

                0: "SELL",
                1: "HOLD",
                2: "BUY"

            }

            return {

                "signal":

                    mapping[
                        signal
                    ],

                "confidence":

                    confidence,

                "take_profit":

                    float(
                        outputs["tp"]
                    ),

                "stop_loss":

                    float(
                        outputs["sl"]
                    ),

                "market_regime":

                    int(

                        outputs[
                            "regime"
                        ].argmax()

                    )

            }