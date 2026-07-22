class ExposureManager:

    def exposure(self, portfolio):

        total = portfolio.total_value()

        exposure = {}

        for p in portfolio.positions.values():

            exposure[p.symbol] = (

                p.current_price *

                p.quantity /

                total

            )

        return exposure