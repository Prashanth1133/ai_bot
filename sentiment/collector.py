from abc import ABC, abstractmethod


class SocialCollector(ABC):

    @abstractmethod
    async def collect(self):

        pass