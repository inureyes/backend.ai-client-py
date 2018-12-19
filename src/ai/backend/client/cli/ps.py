import click

from . import main
from .admin.sessions import sessions


@main.command()
@click.option('--id-only', is_flag=True, help='Display session ids only.')
@click.pass_context
def ps(ctx, id_only):
    '''
    Lists the current running compute sessions for the current keypair.
    This is an alias of the "admin sessions --status=RUNNING" command.
    '''
    ctx.forward(sessions)
