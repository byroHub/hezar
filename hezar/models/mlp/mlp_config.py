from dataclasses import dataclass

from hezar.configs import ModelConfig


@dataclass
class MLPConfig(ModelConfig):
    name: str = "mlp"
    input_shape: int = 4
    output_shape: int = 2
