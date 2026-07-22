from sklearn.model_selection import (
    GridSearchCV
)

import xgboost as xgb


params = {

    "max_depth":
    [4, 6, 8],

    "n_estimators":
    [100, 300, 500],

    "learning_rate":
    [0.1, 0.05]
}


def search(
    X,
    y
):

    model = (
        xgb.XGBClassifier()
    )

    grid = (
        GridSearchCV(
            model,
            params,
            cv=3,
            verbose=1
        )
    )

    grid.fit(
        X,
        y
    )

    return (
        grid.best_params_
    )