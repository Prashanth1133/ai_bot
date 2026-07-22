from abc import ABC, abstractmethod


class NewsCollector(ABC):

    @abstractmethod
    async def collect(self):

        pass