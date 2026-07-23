from training.production_train import (
    ProductionTrain
)


ProductionTrain().train(

    path=

    "data/raw/ETHUSDT.csv",

    save_path=

    "models/eth_production_v1.pt",

    epochs=500

)