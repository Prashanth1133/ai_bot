from training.labels.future_analyzer import (
    FutureAnalyzer
)

from training.labels.reward_risk import (
    RewardRiskCalculator
)

from training.labels.target_builder import (
    TrainingTarget
)


class ProfessionalLabelGenerator:

    def __init__(self):

        self.future = FutureAnalyzer()

        self.rr = RewardRiskCalculator()

    def generate(

        self,

        candles,

        index

    ):

        future = self.future.analyze(

            candles,

            index

        )

        if future is None:

            return None

        reward, risk = self.rr.calculate(

            future["entry"],

            future["highest"],

            future["lowest"]

        )

        if reward > 0.03 and reward > risk*2:

            direction = 2

        elif risk > reward*2:

            direction = 0

        else:

            direction = 1

        confidence = min(

            1.0,

            reward*20

        )

        return TrainingTarget(

            direction=direction,

            confidence=confidence,

            tp=reward,

            sl=risk,

            regime=0
        )