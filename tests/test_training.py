from pathlib import Path


def test_production_training_file_exists():
    assert Path("models/Production/best_model.pt").is_file()
