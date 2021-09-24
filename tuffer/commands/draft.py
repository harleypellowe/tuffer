import os
from typing import Optional
from typing import List

import click

from tuffer import config
from tuffer.ui.parameter.common import integration_option
from tuffer.ui.parameter.common import username_option
from tuffer.models.post import Post
from tuffer.models.post_2 import PostSchema

DRAFT_DIR = os.path.join(config.get("content_dir", ""), "drafts")


@click.group(invoke_without_command=True)
@click.pass_context
def draft(ctx: click.Context):
    """Manage draft posts"""

    if ctx.invoked_subcommand:
        return

    click.echo("Manage draft posts")


@draft.command()
@integration_option
@username_option
def view(integration: Optional[List[str]], username: Optional[List[str]]):
    """List draft posts"""

    click.echo("Drafts:")
    drafts = [
        os.path.join(DRAFT_DIR, x)
        for x in os.listdir(DRAFT_DIR)
        if x[-5:] == ".yaml"
    ]
    for draft in drafts:
        try:
            with open(draft, "r") as infile:
                post_data = infile.read()
        except IOError:
            continue

        post = PostSchema().load(post_data)
        click.echo("---")
        click.echo(f"Title: {post.title}")
        click.echo(f"Text: {post.text}")
        click.echo(f"Tags: {', '.join(post.tags)}")
        click.echo(f"Integrations: {', '.join(post.integrations)}")
        click.echo(f"Publish date: {post.publish_date}")


@draft.command()
@integration_option
@username_option
def remove(integration: Optional[List[str]], username: Optional[List[str]]):
    """Remove a draft post"""

    pass


@draft.command()
@click.argument("integration", type=str)
def add(integration: str):
    """Add a draft post"""

    pass


@draft.command()
@click.argument("integration", type=str)
def edit(integration: str):
    """Edit a draft post"""

    pass


@draft.command()
@click.argument("integration", type=str)
def schedule(integration: str):
    """Schedule a draft post"""

    pass


@draft.command()
@click.argument("integration", type=str)
def publish(integration: str):
    """Publish a draft post"""

    pass
