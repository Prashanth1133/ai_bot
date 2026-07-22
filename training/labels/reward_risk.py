class RewardRiskCalculator:

    def calculate(

        self,

        entry,

        highest,

        lowest

    ):

        reward = (

            highest-entry

        ) / entry

        risk = (

            entry-lowest

        ) / entry

        return reward, risk