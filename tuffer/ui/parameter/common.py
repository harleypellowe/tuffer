import click

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
