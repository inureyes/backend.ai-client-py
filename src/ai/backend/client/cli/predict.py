from argparse import Namespace

from . import register_command
from .admin.sessions import sessions
import subprocess
from .pretty import (
    print_info, print_wait, print_done, print_fail, print_warn,
    format_info,
)

def _noop(*args, **kwargs):
    pass


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
    model_name = 'resnet_v2'

    if args.info:
        if args.detail:
            proc = subprocess.run(
                ['backend.ai run python-tensorflow:1.12-py36-srv ./serving_client.py --mount model_'+model_name+' --exec "python serving_client.py '+model_name+' '+args.payload+' --info --detail" -t '+args.sess], shell=True)    
        else:
            proc = subprocess.run(
                ['backend.ai run python-tensorflow:1.12-py36-srv ./serving_client.py --mount model_'+model_name+' --exec "python serving_client.py '+model_name+' '+args.payload+' --info" -t '+args.sess], shell=True)    
    else:
        proc = subprocess.run(
            ['backend.ai run python-tensorflow:1.12-py36-srv ./serving_client.py --mount model_'+model_name+' --exec "python serving_client.py '+model_name+' '+args.payload+'" -t '+args.sess], shell=True)


predict.add_argument('sess',
                 help='Specify a model serving session ID or name. ')
predict.add_argument('payload',
                 help='Prediction payload.')
predict.add_argument('-i', '--info',  action='store_true', default=False,
                 help='Model information of given session ID')
predict.add_argument('-d', '--detail',  action='store_true', default=False,
                 help='Detailed model information of given session ID')
predict.add_argument('-q', '--quiet', action='store_true', default=False,
                 help='Hide execution details but show only the kernel outputs.')
