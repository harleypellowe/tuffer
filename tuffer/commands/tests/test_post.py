import yaml
import os
import tempfile
from pytest_mock import MockerFixture

from tuffer.models.post import Post
from tuffer.commands.tests.fixtures import mock_post
from tuffer.commands.tests.fixtures import post_yaml


class TestPost:
    def test_post_load(self):
        data = yaml.safe_load(post_yaml)
        post = Post(**data)
        assert post.title == data["title"]
        assert post.text == data["text"]
        assert post.tags == data["tags"]
        assert post.integrations == data.get("integrations", [])

    def test_post_save(self, mocker: MockerFixture, mock_post):
        tmpdir = tempfile.TemporaryDirectory().name

        def mock_save_dir(self):
            return tmpdir

        mocker.patch.object(mock_post, "save_dir", mock_save_dir)
        mock_post.save()
        print(os.listdir(tmpdir))
        assert os.path.exists(os.path.join(tmpdir, mock_post.filename))
