import numpy as np


class CorrelationMatrix:

    def __init__(self):

        self.matrix = {}

    def update(

        self,

        dataframe,

    ):

        self.matrix = dataframe.corr()

    def correlation(

        self,

        a,

        b,

    ):

        return self.matrix.loc[a, b]