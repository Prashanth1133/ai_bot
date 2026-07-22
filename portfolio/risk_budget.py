from dataclasses import dataclass


@dataclass(slots=True)
class RiskBudget:

    maximum_risk: float

    allocated_risk: float = 0.0

    available_risk: float = 0.0