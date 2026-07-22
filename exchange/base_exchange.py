from __future__ import annotations

from abc import ABC
from abc import abstractmethod


class BaseExchange(ABC):

    @abstractmethod
    async def connect(self):
        ...

    @abstractmethod
    async def disconnect(self):
        ...

    @abstractmethod
    async def place_order(self, **kwargs):
        ...

    @abstractmethod
    async def cancel_order(self, order_id):
        ...

    @abstractmethod
    async def get_order(self, order_id):
        ...

    @abstractmethod
    async def account(self):
        ...

    @abstractmethod
    async def positions(self):
        ...

    @abstractmethod
    async def balances(self):
        ...

    @abstractmethod
    async def ticker(self, symbol):
        ...