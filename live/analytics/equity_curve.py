from __future__ import annotations


class EquityCurve:

    def __init__(self):

        self.points = []

    ##########################################################

    def add(

        self,

        timestamp,

        equity,

    ):

        self.points.append(

            (

                timestamp,

                equity,

            )

        )

    ##########################################################

    def latest(self):

        if not self.points:

            return None

        return self.points[-1]

    ##########################################################

    def values(self):

        return self.points

    ##########################################################

    def reset(self):

        self.points.clear()