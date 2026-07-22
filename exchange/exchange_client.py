from __future__ import annotations

from abc import ABC
from abc import abstractmethod


class ExchangeClient(ABC):

    #######################################################

    @abstractmethod
    async def connect(self):
        ...

    #######################################################

    @abstractmethod
    async def disconnect(self):
        ...

    #######################################################

    @abstractmethod
    async def place_order(

        self,

        order,

    ):
        ...

    #######################################################

    @abstractmethod
    async def cancel_order(

        self,

        order_id,

    ):
        ...

    #######################################################

    @abstractmethod
    async def modify_order(

        self,

        order_id,

        **kwargs,

    ):
        ...

    #######################################################

    @abstractmethod
    async def account(self):
        ...

    #######################################################

    @abstractmethod
    async def positions(self):
        ...

    #######################################################

    @abstractmethod
    async def open_orders(self):
        ...