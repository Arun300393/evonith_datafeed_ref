import yaml
import os
from pathlib import Path

def load_config(config_path: str = "src/config/setting.yaml"):
    """
    Load configuration from a YAML file.
    """
    with open(config_path, "r") as file:
        return yaml.safe_load(file)
