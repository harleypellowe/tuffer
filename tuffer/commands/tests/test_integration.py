import pytest
import yaml
from click.testing import CliRunner
from pytest_mock import MockerFixture

from tuffer import config
from tuffer.commands.integration import integration
from tuffer.commands.integration import view
from tuffer.commands.integration import remove


@pytest.fixture
def mock_config():
    config_yaml = """
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
    config_data = yaml.load(config_yaml, Loader=yaml.SafeLoader)
    config.clear()
    config.update(config_data)

    def save():
        return True

    config.save = save

    return config


class TestIntegration:
    runner: CliRunner = CliRunner()

    def test_integration(self):
        result = self.runner.invoke(integration)
        assert result.exit_code == 0
        assert "Manage" in result.output

    def test_view_all(self, mocker: MockerFixture, mock_config):
        mocker.patch.dict("tuffer.config", mock_config)
        result = self.runner.invoke(view)
        assert result.exit_code == 0
        assert "username: Twitter_Alpha" in result.output
        assert "oauth_token: xxx" in result.output
        assert "oauth_token_secret: xxx" in result.output
        assert "username: LinkedIn_Alpha" in result.output

    def test_view_specific_integration(
        self, mocker: MockerFixture, mock_config
    ):
        mocker.patch.dict("tuffer.config", mock_config)
        result = self.runner.invoke(view, ["--integration=twitter"])
        assert result.exit_code == 0
        assert "Twitter_Alpha" in result.output
        assert "Twitter_Beta" in result.output
        assert "LinkedIn_Alpha" not in result.output

        result = self.runner.invoke(
            view, ["--integration=twitter", "--integration=linkedin"]
        )
        assert result.exit_code == 0
        assert "Twitter_Alpha" in result.output
        assert "Twitter_Beta" in result.output
        assert "LinkedIn_Alpha" in result.output

    def test_view_specific_username(self, mocker: MockerFixture, mock_config):
        mocker.patch.dict("tuffer.config", mock_config)
        result = self.runner.invoke(view, ["--username=Twitter_Beta"])
        assert result.exit_code == 0
        assert "Twitter_Alpha" not in result.output
        assert "LinkedIn_Alpha" not in result.output
        assert "Twitter_Beta" in result.output

        result = self.runner.invoke(
            view, ["--username=Twitter_Beta", "--username=LinkedIn_Alpha"]
        )
        assert result.exit_code == 0
        assert "Twitter_Alpha" not in result.output
        assert "LinkedIn_Alpha" in result.output
        assert "Twitter_Beta" in result.output

    def test_remove_all(self, mocker: MockerFixture, mock_config):
        mocker.patch.dict("tuffer.config", mock_config)
        result = self.runner.invoke(remove)
        assert result.exit_code == 0
        from tuffer import config

        assert config["integrations"] == dict()

    def test_remove_one_integration(self, mocker: MockerFixture, mock_config):
        mocker.patch.dict("tuffer.config", mock_config)
        self.runner.invoke(remove, ["--integration=twitter"])
        from tuffer import config

        assert "twitter" not in config["integrations"].keys()
        assert "linkedin" in config["integrations"].keys()

    def test_remove_multiple_integrations(
        self, mocker: MockerFixture, mock_config
    ):
        mocker.patch.dict("tuffer.config", mock_config)
        self.runner.invoke(
            remove, ["--integration=twitter", "--integration=linkedin"]
        )
        from tuffer import config

        print(config.items())

        assert "twitter" not in config["integrations"].keys()
        assert "linkedin" not in config["integrations"].keys()

    def test_remove_one_username(self, mocker: MockerFixture, mock_config):
        mocker.patch.dict("tuffer.config", mock_config)
        result = self.runner.invoke(remove, ["--username=Twitter_Alpha"])
        assert result.exit_code == 0
        from tuffer import config

        config_as_string = str(config)
        assert "Twitter_Alpha" not in config_as_string
        assert "LinkedIn_Alpha" in config_as_string

    def test_remove_multiple_usernames(
        self, mocker: MockerFixture, mock_config
    ):
        mocker.patch.dict("tuffer.config", mock_config)
        result = self.runner.invoke(
            remove, ["--username=Twitter_Alpha", "--username=LinkedIn_Alpha"]
        )
        assert result.exit_code == 0
        from tuffer import config

        config_as_string = str(config)
        assert "Twitter_Alpha" not in config_as_string
        assert "LinkedIn_Alpha" not in config_as_string

    def test_add_twitter(self, mocker: MockerFixture, mock_config):
        pass
