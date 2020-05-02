from O365 import Account
from .. import staticdefault_client


def init_business(args):
    if args.client_id and args.client_secret:
        credentials = (
            args.client_id,
            args.client_secret
        )
    elif args.clients:
        client = args.clients[args.app]
        credentials = (
            client.get('client_id'),
            client.get('client_secret')
        )
    else:
        credentials = default_client

    account = Account(credentials)
    account.authenticate(scopes=['basic', 'onedrive_all', 'sharepoint_dl'])
    return account
