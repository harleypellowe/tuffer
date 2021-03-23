import json

from click.testing import CliRunner
from pytest_mock import MockerFixture

from tuffer.commands.integration import integrations
from tuffer.commands.integration import view
from tuffer.commands.integration import remove
from tuffer.commands.integration import add
from tuffer.commands.tests.fixtures import mock_filled_config
from tuffer.commands.tests.fixtures import mock_empty_config


class TestIntegration:
    runner: CliRunner = CliRunner()

    def test_integration(self):
        result = self.runner.invoke(integrations)
        assert "Manage" in result.output

    def test_view_all(self, mocker: MockerFixture, mock_filled_config):
        mocker.patch.dict("tuffer.config", mock_filled_config)
        result = self.runner.invoke(view)
        assert "username: Twitter_Alpha" in result.output
        assert "oauth_token: xxx" in result.output
        assert "oauth_token_secret: xxx" in result.output
        assert "username: LinkedIn_Alpha" in result.output

    def test_view_specific_integration(
        self, mocker: MockerFixture, mock_filled_config
    ):
        mocker.patch.dict("tuffer.config", mock_filled_config)
        result = self.runner.invoke(view, ["--integration=twitter"])
        assert "Twitter_Alpha" in result.output
        assert "Twitter_Beta" in result.output
        assert "LinkedIn_Alpha" not in result.output

        result = self.runner.invoke(
            view, ["--integration=twitter", "--integration=linkedin"]
        )
        assert "Twitter_Alpha" in result.output
        assert "Twitter_Beta" in result.output
        assert "LinkedIn_Alpha" in result.output

    def test_view_specific_username(
        self, mocker: MockerFixture, mock_filled_config
    ):
        mocker.patch.dict("tuffer.config", mock_filled_config)
        result = self.runner.invoke(view, ["--username=Twitter_Beta"])
        assert "Twitter_Alpha" not in result.output
        assert "LinkedIn_Alpha" not in result.output
        assert "Twitter_Beta" in result.output

        result = self.runner.invoke(
            view, ["--username=Twitter_Beta", "--username=LinkedIn_Alpha"]
        )
        assert "Twitter_Alpha" not in result.output
        assert "LinkedIn_Alpha" in result.output
        assert "Twitter_Beta" in result.output

    def test_remove_all(self, mocker: MockerFixture, mock_filled_config):
        mocker.patch.dict("tuffer.config", mock_filled_config)
        self.runner.invoke(remove)
        from tuffer import config

        assert config["integrations"] == dict()

    def test_remove_one_integration(
        self, mocker: MockerFixture, mock_filled_config
    ):
        mocker.patch.dict("tuffer.config", mock_filled_config)
        self.runner.invoke(remove, ["--integration=twitter"])
        from tuffer import config

        assert "twitter" not in config["integrations"].keys()
        assert "linkedin" in config["integrations"].keys()

    def test_remove_multiple_integrations(
        self, mocker: MockerFixture, mock_filled_config
    ):
        mocker.patch.dict("tuffer.config", mock_filled_config)
        self.runner.invoke(
            remove, ["--integration=twitter", "--integration=linkedin"]
        )
        from tuffer import config

        assert "twitter" not in config["integrations"].keys()
        assert "linkedin" not in config["integrations"].keys()

    def test_remove_one_username(
        self, mocker: MockerFixture, mock_filled_config
    ):
        mocker.patch.dict("tuffer.config", mock_filled_config)
        self.runner.invoke(remove, ["--username=Twitter_Alpha"])
        from tuffer import config

        config_as_string = json.dumps(config)
        assert "Twitter_Alpha" not in config_as_string
        assert "LinkedIn_Alpha" in config_as_string

    def test_remove_multiple_usernames(
        self, mocker: MockerFixture, mock_filled_config
    ):
        mocker.patch.dict("tuffer.config", mock_filled_config)
        self.runner.invoke(
            remove, ["--username=Twitter_Alpha", "--username=LinkedIn_Alpha"]
        )
        from tuffer import config

        config_as_string = json.dumps(config)
        assert "Twitter_Alpha" not in config_as_string
        assert "LinkedIn_Alpha" not in config_as_string

    def test_add(self, mocker: MockerFixture, mock_empty_config):
        # TWITTER
        input_values = ["Twitter_123", "abc", "foo"]
        output = []

        def mock_input(s):
            output.append(s)
            return input_values.pop(0)

        mocker.patch.dict("tuffer.config", mock_empty_config)
        mocker.patch("tuffer.commands.integration.input", mock_input)
        mocker.patch(
            "tuffer.commands.integration.print", lambda s: output.append(s)
        )
        self.runner.invoke(add, ["twitter"])
        assert output == ["Username: ", "OAuth token: ", "OAuth token secret: "]

        from tuffer import config

        assert config.get("integrations") is not None
        assert config["integrations"].get("twitter") is not None
        assert len(config["integrations"]["twitter"]) == 1
        assert (
            config["integrations"]["twitter"][0].get("username")
            == "Twitter_123"
        )
        assert config["integrations"]["twitter"][0].get("oauth_token") == "abc"
        assert (
            config["integrations"]["twitter"][0].get("oauth_token_secret")
            == "foo"
        )
