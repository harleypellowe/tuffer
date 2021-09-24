import pytest
import yaml

from tuffer import config
from tuffer.config import Config
from tuffer.models.post import Post

post_yaml = """
title: Feature release FY21 Q2
text: >-
  Woohoo! We just release a whole new set of features. Check them out here:
  www.example.com
tags:
  - saas
  - newfeatures
  - excited
"""


@pytest.fixture
def mock_post() -> Post:
    data = yaml.safe_load(post_yaml)
    return Post(**data)


def create_config_obj(config_yaml: str) -> Config:
    config_data = yaml.load(config_yaml, Loader=yaml.SafeLoader) or {}
    config.clear()
    config.update(config_data)

    def save():
        return True

    config.save = save

    return config


@pytest.fixture
def mock_filled_config() -> Config:
    config_yaml = """
content_dir: content
integrations:
  twitter:
    accounts:
      - oauth_token: xxx
        oauth_token_secret: xxx
        username: Twitter_Alpha
      - oauth_token: xxx
        oauth_token_secret: xxx
        username: Twitter_Beta
    app:
      consumer_key: xxx
      consumer_key_secret: xxx
  linkedin:
    accounts:
      - username: LinkedIn_Alpha
        password: xxx

"""
    return create_config_obj(config_yaml)


@pytest.fixture
def mock_empty_config() -> Config:
    return create_config_obj("")
