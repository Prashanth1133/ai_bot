import torch

from evaluation.metrics import Metrics


class Validator:

    def __init__(

        self,
        model,
        dataloader

    ):

        self.model = model

        self.loader = dataloader


    @torch.no_grad()
    def validate(self):

        self.model.eval()

        direction_score = []
        reversal_score = []
        regime_score = []

        volatility_score = []
        tp_score = []
        sl_score = []


        for x, y in self.loader:

            outputs = self.model(x)


            direction_score.append(

                Metrics.direction_accuracy(

                    outputs["direction"],
                    y["direction"]

                )

            )


            reversal_score.append(

                Metrics.reversal_accuracy(

                    outputs["reversal"],
                    y["reversal"]

                )

            )


            regime_score.append(

                Metrics.regime_accuracy(

                    outputs["market_regime"],
                    y["market_regime"]

                )

            )


            volatility_score.append(

                Metrics.mse(

                    outputs["volatility"]
                    .squeeze(),

                    y["volatility"]

                )

            )


            tp_score.append(

                Metrics.mse(

                    outputs["take_profit"]
                    .squeeze(),

                    y["take_profit"]

                )

            )


            sl_score.append(

                Metrics.mse(

                    outputs["stop_loss"]
                    .squeeze(),

                    y["stop_loss"]

                )

            )


        Metrics.print_metrics(

            sum(direction_score)/
            len(direction_score),

            sum(reversal_score)/
            len(reversal_score),

            sum(regime_score)/
            len(regime_score),

            sum(volatility_score)/
            len(volatility_score),

            sum(tp_score)/
            len(tp_score),

            sum(sl_score)/
            len(sl_score)

        )