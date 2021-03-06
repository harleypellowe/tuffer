import os
from typing import ClassVar
from dataclasses import dataclass

import yaml


@dataclass
class Config(dict):
    CONFIG_FILENAME: ClassVar[str] = "config.yaml"

    def __post_init__(self):
        super(Config, self).__init__()
        self.load()

    def load(self) -> None:
        if not os.path.exists(self.CONFIG_FILENAME):
            return None

        with open(self.CONFIG_FILENAME, "r") as config_file:
            data = yaml.load(config_file, Loader=yaml.SafeLoader)
            self.update(data)

    def save(self) -> None:
        with open(self.CONFIG_FILENAME, "w") as config_file:
            yaml.dump(dict(self.items()), config_file)
