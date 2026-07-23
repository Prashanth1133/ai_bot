from training.production_train import (
    ProductionTrain
)


ProductionTrain().train(

    path=

    "data/raw/BTCUSDT.csv",

    save_path=

    "models/btc_production_v1.pt",

    epochs=500

)