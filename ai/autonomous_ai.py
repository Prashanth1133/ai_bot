import time


class AutonomousAI:

    """
    Fully autonomous loop.

    Responsibilities:

    1. Predict
    2. Execute
    3. Learn
    4. Retrain
    5. Save checkpoints
    """

    def __init__(

        self,
        ai_engine,
        self_learning,
        online_trainer,
        checkpoint_manager

    ):

        self.ai_engine = ai_engine

        self.self_learning = (

            self_learning

        )

        self.online_trainer = (

            online_trainer

        )

        self.checkpoints = (

            checkpoint_manager

        )

        self.cycles = 0

    def step(

        self,
        state,
        trade=None

    ):

        prediction = (

            self.ai_engine.process(
                state
            )

        )

        if trade:

            reward = (

                self.self_learning

                .record_trade(

                    state,

                    prediction[
                        "signal"
                    ],

                    trade

                )

            )

        else:

            reward = 0

        self.cycles += 1

        if (

            self.cycles % 100

        ) == 0:

            self.online_trainer.train_step()

        if (

            self.cycles % 500

        ) == 0:

            self.checkpoints.save()

        return {

            "prediction":

                prediction,

            "reward":

                reward,

            "cycles":

                self.cycles

        }

    def statistics(self):

        stats = (

            self.self_learning

            .statistics()

        )

        stats["cycles"] = (

            self.cycles

        )

        return stats