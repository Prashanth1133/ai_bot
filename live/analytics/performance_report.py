from __future__ import annotations


class PerformanceReport:

    def generate(

        self,

        statistics,

        equity_curve,

    ):

        return {

            "statistics": statistics.summary(),

            "equity_curve": equity_curve.values(),

        }