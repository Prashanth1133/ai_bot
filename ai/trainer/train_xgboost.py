import joblib
import xgboost as xgb

from sklearn.model_selection import (
    train_test_split
)
from sklearn.metrics import (
    classification_report
)

from ai.dataset.builder import (
    DatasetBuilder
)

builder = DatasetBuilder()

X, y, _ = builder.build(
    "storage/BTCUSDT/1m.parquet"
)

X_train, X_test, y_train, y_test = (
    train_test_split(
        X,
        y,
        test_size=0.2,
        shuffle=False
    )
)

model = xgb.XGBClassifier(
    n_estimators=500,
    max_depth=8,
    learning_rate=0.05,
    objective="multi:softprob",
    num_class=3,
)

model.fit(
    X_train,
    y_train + 1
)

predictions = model.predict(
    X_test
)

print(
    classification_report(
        y_test + 1,
        predictions
    )
)

joblib.dump(
    model,
    "models/xgb_model.pkl"
)