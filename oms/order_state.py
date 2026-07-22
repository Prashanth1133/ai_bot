from enum import Enum


class OrderState(Enum):

    NEW = "NEW"

    SUBMITTED = "SUBMITTED"

    PARTIALLY_FILLED = "PARTIALLY_FILLED"

    FILLED = "FILLED"

    CANCELLED = "CANCELLED"

    REJECTED = "REJECTED"

    EXPIRED = "EXPIRED"