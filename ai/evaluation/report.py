from ai.evaluation.classification import ClassificationMetrics
from ai.evaluation.trading_metrics import TradingMetrics


class EvaluationReport:

    def __init__(self):

        self.classification = ClassificationMetrics()

        self.trading = TradingMetrics()

    def build(

        self,

        y_true,

        y_pred,

        trades,

    ):

        report = {}

        report.update(

            self.classification.evaluate(

                y_true,

                y_pred,

            )

        )

        report.update(

            self.trading.evaluate(

                trades,

            )

        )

        return report