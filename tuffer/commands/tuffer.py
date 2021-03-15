import os

import click

from tuffer import config
from tuffer.commands.help import help
from tuffer.commands.pull import pull
from tuffer.commands.push import push
from tuffer.commands.draft import draft
from tuffer.commands.publish import publish
from tuffer.commands.platform import platform
from tuffer.commands.schedule import schedule


def try_init_content_dir(content_dir: click.Path):
    for folder in [
        content_dir,
        f"{content_dir}/drafts",
        f"{content_dir}/scheduled",
        f"{content_dir}/published",
    ]:
        if not os.path.exists(folder):
            os.mkdir(folder)


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

    content_dir = content_dir or config.get("content_dir")
    if content_dir is None:
        content_dir = "content"
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
tuffer.add_command(platform)
tuffer.add_command(schedule)
