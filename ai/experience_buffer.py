from collections import deque
import random


class ExperienceBuffer:

    def __init__(

        self,
        max_size=100000

    ):

        self.buffer = deque(
            maxlen=max_size
        )

    def add(

        self,
        state,
        action,
        reward,
        next_state,
        done

    ):

        self.buffer.append(

            {

                "state": state,
                "action": action,
                "reward": reward,
                "next_state": next_state,
                "done": done

            }

        )

    def sample(

        self,
        batch_size=128

    ):

        return random.sample(

            self.buffer,

            min(
                batch_size,
                len(self.buffer)
            )

        )

    def __len__(self):

        return len(
            self.buffer
        )