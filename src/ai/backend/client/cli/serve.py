from argparse import Namespace

from . import register_command
from .admin.sessions import sessions
from .pretty import (
    print_info, print_wait, print_done, print_fail, print_warn,
    format_info,
)

import subprocess

@register_command
def serve(args):
    '''
    Serves deep learning models on the fly.
    Currently supports Servable models for TensorFlow Serving.
    '''
    if args.quiet:
        vprint_info = vprint_wait = vprint_done = _noop
    else:
        vprint_info = print_info
        vprint_wait = print_wait
        vprint_done = print_done
    vprint_info("Loading model: "+args.model)
    model_name = args.model
    proc = subprocess.run(
        ['backend.ai run python-tensorflow:1.12-py36-serv --mount model_'+model_name+' -c "print(\' - Model loaded.\')"'], shell=True)

serve.add_argument('model',
                 help='Serving model name. ')
serve.add_argument('-q', '--quiet', action='store_true', default=False,
                 help='Hide execution details but show only the kernel outputs.')