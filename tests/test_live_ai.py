import torch

from live.live_ai_engine import (
    LiveAIEngine
)

def test_live_ai_loads_production_model():
    result = LiveAIEngine("models/Production/best_model.pt").predict(torch.randn(128, 11))
    assert {"signal", "confidence", "take_profit", "stop_loss"} <= set(result)
