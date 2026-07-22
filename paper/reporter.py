from __future__ import annotations


class PaperReporter:

    def report(

        self,

        portfolio,

        statistics,

    ):

        return {

            "portfolio": portfolio.snapshot(),

            "statistics": statistics.summary(),

        }