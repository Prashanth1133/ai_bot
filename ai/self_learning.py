import time

from ai.experience_buffer import ExperienceBuffer
from ai.reward_engine import RewardEngine


class SelfLearningEngine:

    """
    Responsible for:
    - Recording every AI decision
    - Computing rewards
    - Building experience memory
    - Tracking AI performance
    - Providing statistics for retraining
    """

    def __init__(

        self,
        buffer=None,
        reward_engine=None

    ):

        self.buffer = buffer or ExperienceBuffer()

        self.reward_engine = (

            reward_engine
            or RewardEngine()

        )

        self.samples = 0
        self.correct = 0

        self.total_reward = 0.0

        self.started = time.time()

    def update(

        self,
        prediction,
        actual

    ):

        """
        prediction:
            BUY/HOLD/SELL

        actual:
            BUY/HOLD/SELL
        """

        self.samples += 1

        is_correct = (

            prediction ==
            actual

        )

        if is_correct:

            self.correct += 1

        return {

            "samples":

                self.samples,

            "correct":

                self.correct,

            "accuracy":

                self.accuracy(),

            "prediction":

                prediction,

            "actual":

                actual

        }

    def record_trade(

        self,
        state,
        action,
        trade

    ):

        """
        Trade object requires:

        trade.pnl
        trade.next_state
        """

        reward = (

            self.reward_engine.compute(
                trade
            )

        )

        self.total_reward += reward

        self.buffer.add(

            state=state,

            action=action,

            reward=reward,

            next_state=trade.next_state,

            done=True

        )

        return reward

    def accuracy(self):

        if self.samples == 0:

            return 0.0

        return (

            self.correct /
            self.samples

        )

    def average_reward(self):

        if len(self.buffer) == 0:

            return 0.0

        return (

            self.total_reward /
            len(self.buffer)

        )

    def uptime(self):

        return (

            time.time() -
            self.started

        )

    def statistics(self):

        return {

            "samples":

                self.samples,

            "correct":

                self.correct,

            "accuracy":

                round(

                    self.accuracy(),

                    4

                ),

            "avg_reward":

                round(

                    self.average_reward(),

                    4

                ),

            "experience_size":

                len(
                    self.buffer
                ),

            "uptime_seconds":

                int(
                    self.uptime()
                )

        }

    def reset(self):

        self.samples = 0
        self.correct = 0
        self.total_reward = 0.0

        self.buffer = ExperienceBuffer()