import os

import click

from tuffer import config
from tuffer.commands.help import help
from tuffer.commands.pull import pull
from tuffer.commands.push import push
from tuffer.commands.draft import draft
from tuffer.commands.publish import publish
from tuffer.commands.integration import integrations
from tuffer.commands.schedule import schedule


def try_init_content_dir(content_dir: str):
    for folder in ["drafts", "scheduled", "published"]:
        print(os.path.join(content_dir, folder))
        os.makedirs(os.path.join(content_dir, folder), exist_ok=True)


@click.group(invoke_without_command=True)
@click.version_option(message="%(prog)s %(version)s")
@click.option(
    "--content-dir",
    help=(
        "A path to the folder where content will be stored. Default: ./content."
    ),
)
@click.pass_context
def tuffer(ctx: click.Context, content_dir: click.Path = None):
    if ctx.invoked_subcommand:
        return

    content_dir = content_dir or config.get("content_dir") or "content"
    config["content_dir"] = content_dir
    config.save()
    try_init_content_dir(content_dir)

    click.echo(
        "Welcome to Tuffer, a free open-source tool for creating and "
        "scheduling social media posts from the terminal."
    )


tuffer.add_command(help)
tuffer.add_command(pull)
tuffer.add_command(push)
tuffer.add_command(draft)
tuffer.add_command(publish)
tuffer.add_command(integrations)
tuffer.add_command(schedule)
