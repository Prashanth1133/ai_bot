from collections import defaultdict

from smart_money.order_block_types import (
    OrderBlockStatus,
)


class OrderBlockManager:

    def __init__(self):

        self.blocks = defaultdict(list)

    def add(

        self,

        block

    ):

        self.blocks[block.symbol].append(block)

    def active(

        self,

        symbol

    ):

        return [

            b

            for b in self.blocks[symbol]

            if b.status == OrderBlockStatus.ACTIVE

        ]

    def update(

        self,

        symbol,

        price

    ):

        for block in self.blocks[symbol]:

            if block.status != OrderBlockStatus.ACTIVE:

                continue

            if block.low <= price <= block.high:

                block.status = OrderBlockStatus.MITIGATED