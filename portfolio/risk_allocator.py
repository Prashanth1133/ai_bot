from portfolio.risk_budget import RiskBudget


class RiskAllocator:

    def allocate(

        self,

        maximum,

        requests,

    ):

        budget = RiskBudget(

            maximum_risk=maximum,

            available_risk=maximum,

        )

        total = sum(requests)

        if total == 0:

            return budget

        budget.allocated_risk = min(

            total,

            maximum,

        )

        budget.available_risk = (

            maximum

            - budget.allocated_risk

        )

        return budget