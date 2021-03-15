import os
import shutil
from typing import List

from click.testing import CliRunner
from pytest_mock import MockerFixture

from tuffer.commands.tuffer import tuffer


def get_content_paths(root: str, content_dir: str = "content") -> List[str]:
    return [
        os.path.join(root, content_dir, folder)
        for folder in ["drafts", "scheduled", "published"]
    ]


class TestTuffer:
    runner: CliRunner = CliRunner()

    def test_create_content_dir_without_option(self):
        content_dir = "content"
        result = self.runner.invoke(tuffer)

        paths = get_content_paths(os.getcwd())
        for path in paths:
            assert os.path.exists(path)

        assert result.exit_code == 0
        assert "Welcome" in result.output

        from tuffer import config

        assert config.get("content_dir") == content_dir

        shutil.rmtree(os.path.join(os.getcwd(), content_dir))

    def test_create_content_dir_with_option(self):
        content_dir = "tuffer"
        result = self.runner.invoke(tuffer, [f"--content-dir={content_dir}"])

        paths = get_content_paths(os.getcwd(), "tuffer")
        for path in paths:
            assert os.path.exists(path)

        assert result.exit_code == 0
        assert "Welcome" in result.output

        from tuffer import config

        assert config.get("content_dir") == content_dir

        shutil.rmtree(os.path.join(os.getcwd(), content_dir))

    def test_create_content_dir_with_config(self, mocker: MockerFixture):
        content_dir = "my_content"

        config = dict(content_dir=content_dir)
        mocker.patch.dict("tuffer.config", config)
        result = self.runner.invoke(tuffer)

        paths = get_content_paths(os.getcwd(), content_dir)
        for path in paths:
            assert os.path.exists(path)

        assert result.exit_code == 0
        assert "Welcome" in result.output

        from tuffer import config

        assert config.get("content_dir") == content_dir

        shutil.rmtree(os.path.join(os.getcwd(), content_dir))
