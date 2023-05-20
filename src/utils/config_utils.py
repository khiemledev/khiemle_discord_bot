from os import getenv
from typing import Any

import dotenv
from hydra import compose, initialize
from omegaconf import DictConfig, OmegaConf

dotenv.load_dotenv()


def parse_value(value: Any) -> Any:
    """
    A helper function that tries to parse a value as an integer, float or boolean.
    If the value cannot be parsed, returns the original value.
    """
    if isinstance(value, str):
        _value = value.strip().lower()
        if _value == "true":
            return True
        elif _value == "false":
            return False
        else:
            try:
                return int(_value)
            except ValueError:
                pass
            try:
                return float(_value)
            except ValueError:
                pass
    return value


def env_resolver(key: str) -> Any:
    value = getenv(key, None)
    return parse_value(value)


OmegaConf.register_new_resolver("env", env_resolver)


def get_config(module_name: str = None) -> DictConfig:
    with initialize(config_path="../config", version_base="v1.1"):
        config = compose("app.yaml")
        if module_name:
            module_config = config.get(module_name, {})
            return module_config
        else:
            return config
