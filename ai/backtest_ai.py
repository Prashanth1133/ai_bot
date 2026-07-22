class AIBacktester:

    def __init__(

        self,
        ai

    ):

        self.ai = ai

        self.trades = []

    def run(

        self,
        dataset

    ):

        wins = 0

        losses = 0

        for state, trade in dataset:

            result = self.ai.step(

                state,

                trade

            )

            if result["reward"] > 0:

                wins += 1

            else:

                losses += 1

            self.trades.append(

                result

            )

        total = wins + losses

        return {

            "trades": total,

            "wins": wins,

            "losses": losses,

            "win_rate":

                wins / total

                if total else 0

        }