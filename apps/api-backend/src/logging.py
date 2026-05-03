import logging.config
import yaml

from src.settings import BASE_DIR


def setup_logging(log_level: str):
    config_file = BASE_DIR / "config" / "logging.yaml"

    with open(config_file, "r") as f:
        config = yaml.safe_load(f)

    for logger_name in config.get("loggers", {}):
        config["loggers"][logger_name]["level"] = log_level

    logging.config.dictConfig(config)

    return config
