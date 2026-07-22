from abc import ABC, abstractmethod


class HistoricalDownloader(ABC):

    @abstractmethod
    def download(

        self,

        symbol,

        timeframe,

        start,

        end

    ):

        pass