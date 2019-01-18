from argparse import Namespace
import click
from . import main

from .admin.sessions import sessions
from .pretty import (
    print_info, print_wait, print_done, print_error, print_fail, print_warn,
    format_info,
)

import subprocess

def _noop(*args, **kwargs):
    pass

@main.command()
@click.argument('model', metavar='MODEL', nargs=1)
@click.option('-q', '--quiet', is_flag=True,
              help='Hide execution details but show only the kernel outputs.')
def serve(model, quiet):
    '''
    Serves deep learning models on the fly.
    Currently supports Servable models for TensorFlow Serving.
    '''
    print(model)
    if quiet:
        vprint_info = vprint_wait = vprint_done = _noop
    else:
        vprint_info = print_info
        vprint_wait = print_wait
        vprint_done = print_done
    vprint_info("Loading model: "+model)
    model_name = model
    proc = subprocess.run(
        ['backend.ai run python-tensorflow:1.12-py36-srv --mount model_'+model_name+'  -e MODEL_NAME='+model_name+' -c "print(\' - Model loaded.\')"'], shell=True)
