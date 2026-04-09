from dataclasses import dataclass
from pathlib import Path

import yaml


@dataclass
class DoughyConfig:
    # Temperature control
    target_temp: float = 26.0
    deadband: float = 0.5

    # Hardware
    mock_hardware: bool = False
    relay_pin: int = 17
    relay_active_high: bool = True
    mock_ambient_temp: float = 20.0

    # Timing
    read_interval_seconds: float = 10.0
    log_interval_seconds: float = 60.0

    # Storage
    db_path: str = "doughy.db"

    @classmethod
    def load(cls, path: Path) -> "DoughyConfig":
        if path.exists():
            with open(path) as f:
                data = yaml.safe_load(f) or {}
            return cls(**{k: v for k, v in data.items() if k in cls.__dataclass_fields__})
        return cls()
