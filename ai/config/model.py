from dataclasses import dataclass


@dataclass(slots=True)
class ModelConfig:

    # Input

    sequence_length: int = 120

    feature_dimension: int = 128

    symbol_embedding_size: int = 16

    # Transformer

    embedding_dimension: int = 256

    encoder_layers: int = 4

    attention_heads: int = 8

    feed_forward_dimension: int = 512

    dropout: float = 0.10

    # Output

    number_of_classes: int = 3

    # Multi-symbol

    supported_symbols = (

        "BTCUSDT",

        "ETHUSDT",

        "DOGEUSDT",

    )