import dill


def save_session(client, path=''):
    """OneDriveClient, str->None
    
    Save the session info in a pickle file.
    
    Not safe, but whatever.
    """

    # client.auth_provider.save_session(path = path)
    c = dill.dumps(client)
    with open(path, 'wb') as f:
        f.write(c)
    return


def load_session(path=''):
    """str->OneDriveClient
    
    Determine whether the session is a normal or Business one,
    load a session from the storaged pickle,
    then refresh so the session is available to use immediately.
    """
    if not os.path.isfile(path):
        logging.error('Session dump path does not exist')
        raise Exception

    with open(path, 'rb') as f:
        client = dill.load(f)
    return client
