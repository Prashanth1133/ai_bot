import numpy as np


class CorrelationEngine:

    def correlation(self, x, y):

        return np.corrcoef(x, y)[0,1]