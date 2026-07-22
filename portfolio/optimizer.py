class PortfolioOptimizer:

    def allocate(

        self,

        scores

    ):

        total = sum(scores.values())

        return {

            k:v/total

            for k,v in scores.items()

        }