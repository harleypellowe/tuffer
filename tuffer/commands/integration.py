from typing import Optional
from typing import List

import click

from tuffer import config


@click.group(invoke_without_command=True)
@click.pass_context
def integration(ctx: click.Context):
    """Manage integration credentials"""

    if ctx.invoked_subcommand:
        return

    click.echo("Manage integration credentials.")


@integration.command()
@click.option(
    "--integration",
    type=str,
    multiple=True,
    help="The integration to filter results by.",
)
@click.option(
    "--username",
    type=str,
    multiple=True,
    help="The username to filter results by.",
)
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


@integration.command()
@click.option(
    "--integration",
    type=str,
    multiple=True,
    help="Remove all integrations of this type.",
)
@click.option(
    "--username",
    type=str,
    multiple=True,
    help="Remove the integration associated with this username.",
)
def remove(integration: Optional[List[str]], username: Optional[List[str]]):
    """Remove connected integrations"""

    # Delete ALL integrations.
    if not integration and not username:
        config["integrations"] = dict()

    platforms = config.get("integrations")
    for platform, platform_data in platforms.items():

        # Delete all accounts for specified integrations.
        if integration and platform in integration:
            del config["integrations"][platform]
            continue

        # Delete accounts with specific usernames.
        temp_accounts = list()
        for account in platform_data["accounts"]:
            if username and account["username"] in username:
                continue
            temp_accounts.append(account)
        platform_data["accounts"] = temp_accounts
    config.save()
