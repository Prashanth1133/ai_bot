from live.risk.models import (
    RiskViolation,
    RiskSeverity,
)


class LeverageGuard:

    def __init__(

        self,

        maximum: int,

    ):

        self.maximum = maximum

    def check(

        self,

        leverage: int,

    ):

        if leverage > self.maximum:

            return RiskViolation(

                source="LeverageGuard",

                severity=RiskSeverity.CRITICAL,

                message=(
                    f"Maximum leverage "
                    f"{self.maximum}x exceeded"
                ),

            )

        return None