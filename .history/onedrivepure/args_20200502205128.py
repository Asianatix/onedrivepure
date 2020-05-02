import argparse
import json
import os

# Arguments


def parse_args():

    parser = argparse.ArgumentParser()

    # Set the config file location
    parser.add_argument('-chunk',
                        default=10*(1024**2),
                        type=int,)
    parser.add_argument('-workers',
                        default=10,
                        type=int)
    parser.add_argument('-sharelink',
                        action='store_true',
                        default=False)

    parser.add_argument('-step',
                        default=102400,
                        type=int)

    parser.add_argument('-app',
                        default=0,
                        type=int)
    # Set the config file location
    parser.add_argument('-conf',
                        default='./onedrive.json')

    # Script actions
    # Set mutually exclusive actions
    actions = [
        'init_business', 'init', 'get', 'list',
        'put', 'delete', 'mkdir', 'move', 'remote',
        'quota', 'share', 'direct', 'search'
    ]
    parser.add_argument('mode', choices=actions)

    # Return the parsed content
    args, rest = parser.parse_known_args()

    if os.path.exists(args.conf):
        conf = json.load(open(args.conf, 'r'))
        args.conf = conf
        for key, value in conf.items():
            if not args.hasattr(key):
                args.setattr(key, value)
        if not args.client_id or not args.client_secret:
            if not args.clients:
                from .static import client_id, client_secret
                args.client_id = client_id
                args.client_secret = client_secret
            else:
                args.client_id = args.clients[0]
                args.client_secret = client_secret
    args.rest = rest
    return args
