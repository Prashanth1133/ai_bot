from __future__ import annotations


class DecisionValidator:

    VALID_ACTIONS = {
        "BUY",
        "SELL",
        "HOLD",
    }

    def validate(
        self,
        result,
    ) -> bool:

        if result.action not in self.VALID_ACTIONS:
            return False

        if result.confidence < 0:
            return False

        if result.confidence > 1:
            return False

        if result.quantity < 0:
            return False

        return True