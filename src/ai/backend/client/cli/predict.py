from argparse import Namespace

from . import register_command
from .admin.sessions import sessions
import subprocess
from .pretty import (
    print_info, print_wait, print_done, print_fail, print_warn,
    format_info,
)

@register_command
def predict(args):
    '''
    Predict / infer results with given data using serving deep learning models.
    '''
    if args.quiet:
        vprint_info = vprint_wait = vprint_done = _noop
    else:
        vprint_info = print_info
        vprint_wait = print_wait
        vprint_done = print_done
    proc = subprocess.run(
        ['backend.ai run python-tensorflow:1.12-py36-srv ./serving_client.py --mount model_'+model_name+' --exec "python serving_client.py '+args.payload+'" -t '+args.sess], shell=True)


predict.add_argument('sess',
                 help='Specify a model serving session ID or name. ')
predict.add_argument('payload',
                 help='Prediction payload.')
predict.add_argument('--info', metavar='INFO',
                 help='Model information of given session ID')
predict.add_argument('-q', '--quiet', action='store_true', default=False,
                 help='Hide execution details but show only the kernel outputs.')
