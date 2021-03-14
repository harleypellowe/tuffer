import os

import yaml

CONFIG_FILENAME = "config.yaml"


def load_config() -> dict:
    if not os.path.exists(CONFIG_FILENAME):
        return {}

    with open(CONFIG_FILENAME, "r") as config_file:
        return yaml.load(config_file, Loader=yaml.SafeLoader)


def write_config(data) -> None:
    with open(CONFIG_FILENAME, "w") as config_file:
        yaml.dump(data, config_file)
