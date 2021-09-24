import os
import shutil
from typing import List

from click.testing import CliRunner
from pytest_mock import MockerFixture

from tuffer.commands.tuffer import tuffer
from tuffer.config import Config


def get_content_paths(root: str, content_dir: str = "content") -> List[str]:
    return [
        os.path.join(root, content_dir, folder)
        for folder in ["drafts", "scheduled", "published"]
    ]


class TestTuffer:
    runner: CliRunner = CliRunner()

    def test_create_content_dir_without_option(self, mocker: MockerFixture):
        content_dir = "content"
        mock_config = Config()
        mock_config.save = lambda: None
        mocker.patch.dict("tuffer.config", mock_config)
        result = self.runner.invoke(tuffer)

        paths = get_content_paths(os.getcwd())
        for path in paths:
            assert os.path.exists(path)

        assert "Welcome" in result.output

        from tuffer import config

        assert config.get("content_dir") == content_dir

        shutil.rmtree(os.path.join(os.getcwd(), content_dir))

    def test_create_content_dir_with_option(self, mocker: MockerFixture):
        content_dir = "tuffer"
        mock_config = Config()
        mock_config.save = lambda: None
        mocker.patch.dict("tuffer.config", mock_config)
        result = self.runner.invoke(tuffer, [f"--content-dir={content_dir}"])

        paths = get_content_paths(os.getcwd(), content_dir="tuffer")
        for path in paths:
            assert os.path.exists(path)

        assert "Welcome" in result.output

        from tuffer import config

        assert config.get("content_dir") == content_dir

        shutil.rmtree(os.path.join(os.getcwd(), content_dir))

    def test_create_content_dir_with_config(self, mocker: MockerFixture):
        content_dir = "my_content"

        mock_config = Config()
        mock_config["content_dir"] = content_dir
        mock_config.save = lambda: None
        mocker.patch.dict("tuffer.config", mock_config)
        result = self.runner.invoke(tuffer)

        paths = get_content_paths(os.getcwd(), content_dir=content_dir)
        for path in paths:
            assert os.path.exists(path)

        assert "Welcome" in result.output

        from tuffer import config

        assert config.get("content_dir") == content_dir

        shutil.rmtree(os.path.join(os.getcwd(), content_dir))
