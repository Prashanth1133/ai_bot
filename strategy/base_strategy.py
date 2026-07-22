from abc import ABC, abstractmethod


class BaseStrategy(ABC):

    name = "BaseStrategy"

    @abstractmethod
    def generate(self, context):
        raise NotImplementedError