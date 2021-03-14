import click


@click.group(invoke_without_command=True)
@click.pass_context
def pull(ctx: click.Context):
    if ctx.invoked_subcommand:
        return
