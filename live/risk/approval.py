from __future__ import annotations

from live.risk.models import (
    RiskDecision,
    RiskStatus,
    RiskViolation,
)


class ApprovalEngine:

    """
    Collects all violations and
    returns one unified decision.
    """

    def approve(

        self,

        violations: list[RiskViolation],

    ) -> RiskDecision:

        if violations:

            return RiskDecision(

                status=RiskStatus.REJECTED,

                approved=False,

                violations=violations,

            )

        return RiskDecision(

            status=RiskStatus.APPROVED,

            approved=True,

            violations=[],

        )