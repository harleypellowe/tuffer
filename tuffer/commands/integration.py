from typing import Optional
from typing import List

import click

from tuffer import config

integration_option = click.option(
    "--integration",
    type=str,
    multiple=True,
    help="The integration(s) to apply this command to.",
)
username_option = click.option(
    "--username",
    type=str,
    multiple=True,
    help="The username(s) to apply this command to.",
)


@click.group(invoke_without_command=True)
@click.pass_context
def integrations(ctx: click.Context):
    """Manage integration credentials"""

    if ctx.invoked_subcommand:
        return

    click.echo("Manage integration credentials.")


@integrations.command()
@integration_option
@username_option
def view(integration: Optional[List[str]], username: Optional[List[str]]):
    """List connected integrations"""

    platforms = config.get("integrations")
    for platform, platform_data in platforms.items():
        if integration and platform not in integration:
            continue
        for account in platform_data["accounts"]:
            if username and account["username"] not in username:
                continue
            for key, value in account.items():
                print(f"{key}: {value}")


@integrations.command()
@integration_option
@username_option
def remove(integration: Optional[List[str]], username: Optional[List[str]]):
    """Remove connected integrations"""

    # Delete ALL integrations.
    if not integration and not username:
        config["integrations"] = dict()

    # Delete ALL accounts for SPECIFIC integrations.
    if integration:
        platforms_to_delete = [
            x for x in config["integrations"].keys() if x in integration
        ]
        for platform in platforms_to_delete:
            del config["integrations"][platform]

    # Delete SPECIFIC accounts.
    if username:
        platforms = config.get("integrations")
        for platform, platform_data in platforms.items():
            accounts = platform_data["accounts"]
            accounts_to_keep = [
                x for x in accounts if x["username"] not in username
            ]
            platform_data["accounts"] = accounts_to_keep
    config.save()


@integrations.command()
@click.argument("integration", type=str)
def add(integration: str):
    """Add an integration"""

    integration_data = dict()
    if integration == "twitter":
        integration_data["username"] = input("Username: ")
        integration_data["oauth_token"] = input("OAuth token: ")
        integration_data["oauth_token_secret"] = input("OAuth token secret: ")

    if "integrations" not in config.keys():
        config["integrations"] = dict()
    if "twitter" not in config["integrations"]:
        config["integrations"]["twitter"] = list()
    config["integrations"]["twitter"].append(integration_data)
