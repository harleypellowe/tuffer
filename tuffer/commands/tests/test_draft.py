import pytest
import yaml
from click.testing import CliRunner
from pytest_mock import MockerFixture

from tuffer.commands.draft import draft
from tuffer.commands.draft import view
from tuffer.commands.tests.fixtures import mock_filled_config


class TestDraft:
    runner: CliRunner = CliRunner()

    def test_draft(self):
        result = self.runner.invoke(draft)
        assert "Manage" in result.output

    def test_view(self):
        result = self.runner.invoke(view)
        assert "Drafts" in result.output
