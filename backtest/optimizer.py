from __future__ import annotations

from itertools import product
from copy import deepcopy


class ParameterOptimizer:
    """
    Performs parameter optimization for
    strategy and AI configuration.

    Initially supports Grid Search.

    Later versions will support:

    - Bayesian Optimization
    - Optuna
    - HyperOpt
    - Genetic Algorithms
    """

    def __init__(self):

        self.results = []

    def grid_search(

        self,

        parameter_grid: dict,

        evaluation_function,

    ):

        """
        parameter_grid example

        {
            "atr_multiplier":[1.5,2.0,2.5],
            "rr":[2,3,4],
            "risk":[0.005,0.01]
        }
        """

        keys = list(parameter_grid.keys())

        values = list(parameter_grid.values())

        for combination in product(*values):

            params = dict(zip(keys, combination))

            score = evaluation_function(
                deepcopy(params)
            )

            self.results.append(

                {
                    "params": params,
                    "score": score,
                }

            )

        self.results.sort(

            key=lambda x: x["score"],

            reverse=True,

        )

        return self.results

    def best(self):

        if not self.results:

            return None

        return self.results[0]

    def top(self, n=10):

        return self.results[:n]