import os
from typing import List
from typing import Union
from typing import Optional
from dataclasses import dataclass
from dataclasses import field

import arrow
import yaml
from arrow import Arrow

from tuffer import config
from tuffer.models.post_2 import PostSchema

DATE_FORMAT = "YYYY-MM-DD_HH:mm:ss"


@dataclass
class Post:
    title: str = None
    text: str = None
    integrations: List[str] = field(default_factory=list)
    tags: List[str] = field(default_factory=list)

    def __post_init__(self):
        self._publish_date: Optional[Arrow] = None

    # def load(self, filename: str) -> None:
    #     assert filename[-5:] == ".yaml"

    #     with open(filename, "r") as infile:
    #         yaml_data = infile.read()
    #     data = yaml.load(yaml_data, Loader=yaml.SafeLoader)
    #     self.__dict__.update(data)

    def save(self) -> None:
        post_data = PostSchema().dump(self)
        # yaml_data = yaml.dump(
        #     dict(
        #         title=self.title,
        #         text=self.text,
        #         integrations=self.integrations,
        #         tags=self.tags,
        #         publish_date=self.publish_date.format(DATE_FORMAT),
        #     )
        # )
        os.makedirs(self.save_dir, exist_ok=True)
        with open(os.path.join(self.save_dir, self.filename), "w") as outfile:
            outfile.write(post_data)

    @property
    def publish_date(self) -> str:
        return (
            self._publish_date.format(DATE_FORMAT) if self._publish_date else ""
        )

    @publish_date.setter
    def publish_date(self, value: Union[Arrow, str]) -> None:
        if isinstance(value, str):
            self._publish_date = arrow.get(value, DATE_FORMAT)
        elif isinstance(value, Arrow):
            self._publish_date = value

    @property
    def save_dir(self) -> str:
        """The directory to save the post to"""

        content_dir = config["content_dir"]
        # content_dir = os.path.join(os.getcwd(), content_dir)
        if self.is_published:
            return os.path.join(content_dir, "published")
        elif self.is_scheduled:
            return os.path.join(content_dir, "scheduled")
        return os.path.join(content_dir, "drafts")

    @property
    def filename(self) -> str:
        return (
            f"{self._publish_date}_{self.title}.yaml"
            if self.publish_date
            else f"{self.title}.yaml"
        )

    @property
    def is_scheduled(self):
        return self.publish_date

    @property
    def is_published(self):
        return self.publish_date and self.publish_date <= arrow.now()
