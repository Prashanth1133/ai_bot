from abc import ABC, abstractmethod


class OnChainCollector(ABC):

    @abstractmethod
    async def collect(self):

        pass