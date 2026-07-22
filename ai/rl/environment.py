import gymnasium as gym
import numpy as np


class TradingEnv(
    gym.Env
):

    def __init__(
        self,
        prices
    ):

        self.prices = prices

        self.idx = 0

        self.action_space = (
            gym.spaces.Discrete(
                3
            )
        )

        self.observation_space = (
            gym.spaces.Box(
                low=-1,
                high=1,
                shape=(10,)
            )
        )

    def reset(
        self,
        seed=None
    ):

        self.idx = 0

        return (
            np.zeros(10),
            {}
        )

    def step(
        self,
        action
    ):

        self.idx += 1

        done = (
            self.idx
            >= len(
                self.prices
            ) - 1
        )

        reward = 0

        return (
            np.zeros(10),
            reward,
            done,
            False,
            {}
        )