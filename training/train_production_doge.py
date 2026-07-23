from training.production_train import (
    ProductionTrain
)


ProductionTrain().train(

    path=

    "data/raw/DOGEUSDT.csv",

    save_path=

    "models/doge_production_v1.pt",

    epochs=500

)