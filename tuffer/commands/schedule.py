import click


@click.group(invoke_without_command=True)
@click.pass_context
def schedule(ctx: click.Context):
    if ctx.invoked_subcommand:
        return
