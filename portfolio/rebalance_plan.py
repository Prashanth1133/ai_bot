from dataclasses import dataclass, field


@dataclass(slots=True)
class RebalancePlan:

    orders: list = field(default_factory=list)

    turnover: float = 0.0

    estimated_cost: float = 0.0